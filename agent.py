
"""
The FitFindr planning loop.

The loop checks each tool result before deciding what to do next.
If the search returns no listings, it stops before calling the outfit
and fit-card tools.
"""

import config
import trace
import re

from tools import suggest_outfit, create_fit_card
from mcp_client import call_tool
from generate import ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """Create a fresh session for one user interaction."""
    return {
        "query": query,
        "parsed": {},
        "search_results": [],
        "selected_item": None,
        "wardrobe": wardrobe,
        "outfit_suggestion": None,
        "fit_card": None,
        "error": None,
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the planning loop once and return the finished session.

    Branch rule:
    If search_listings returns no results, record an actionable error
    and stop before calling suggest_outfit or create_fit_card.
    """
    session = new_session(query, wardrobe)

    try:
        # Step 1: Parse the query.
        description = query

        price_match = re.search(
            r"\b(?:under|below|less than|up to|max(?:imum)?)\s*\$?(\d+(?:\.\d{1,2})?)",
            query,
            re.IGNORECASE,
        )

        size_match = re.search(
            r"\bsize\s+([A-Za-z0-9]+(?:/[A-Za-z0-9]+)?)",
            query,
            re.IGNORECASE,
        )

        max_price = float(price_match.group(1)) if price_match else None
        size = size_match.group(1) if size_match else None

        if price_match:
            description = description.replace(price_match.group(0), "")

        if size_match:
            description = description.replace(size_match.group(0), "")

        description = re.sub(
            r"^(?:looking for|find me|find|show me|i want|want)\s+",
            "",
            description,
            flags=re.IGNORECASE,
        )

        description = re.sub(r"\s+", " ", description).strip(" ,.")

        session["parsed"] = {
            "description": description,
            "size": size,
            "max_price": max_price,
        }

        trace.step(
            "parse_query",
            inputs={"query": query},
            returned=session["parsed"],
        )

        # Step 2: Search listings through MCP.
        trace.check_iterations(1)

        session["search_results"] = call_tool(
            "search_listings",
            {
                "description": session["parsed"]["description"],
                "size": session["parsed"]["size"],
                "max_price": session["parsed"]["max_price"],
            },
        )

        # Trace step 3: Record the MCP search result.
        trace.step(
            "search_listings (via MCP)",
            inputs=session["parsed"],
            returned=session["search_results"],
        )

        # Branch: stop if the search returned no matches.
        if not session["search_results"]:
            session["error"] = (
                "I couldn't find matching listings. Try using a broader "
                "clothing description, removing the size filter, or "
                "increasing your maximum price."
            )

            # Trace step 4: Record why the loop stopped.
            trace.step(
                "empty_search_branch",
                returned=session["error"],
                note="No listings found; stopping",
            )

            return session

        # Step 3: Select the first result.
        trace.check_iterations(2)

        session["selected_item"] = session["search_results"][0]

        # Trace step 5: Record the selected item.
        trace.step(
            "select_item",
            inputs={
                "result_count": len(session["search_results"]),
            },
            returned=session["selected_item"],
        )

        # Step 4: Suggest an outfit.
        session["outfit_suggestion"] = suggest_outfit(
            session["selected_item"],
            session["wardrobe"],
        )

        # Trace step 6: Record the outfit suggestion.
        trace.step(
            "suggest_outfit",
            inputs={
                "selected_item": session["selected_item"],
                "wardrobe": session["wardrobe"],
            },
            returned=session["outfit_suggestion"],
        )

        # Step 5: Create a fit card.
        trace.check_iterations(3)

        session["fit_card"] = create_fit_card(
            session["outfit_suggestion"],
            session["selected_item"],
        )

        # Trace step 7: Record the completed fit card.
        trace.step(
            "create_fit_card",
            inputs={
                "outfit_suggestion": session["outfit_suggestion"],
                "selected_item": session["selected_item"],
            },
            returned=session["fit_card"],
        )

    except ModelUnavailable as exc:
        session["error"] = (
            f"The model is unavailable: {exc}. "
            "Check your model API key and connection in .env, "
            "then retry with a new query."
        )

    except RuntimeError as exc:
        session["error"] = str(exc)

    return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(
            f"  fit_card is {session['fit_card']!r} "
            "— it should still be None here"
        )
        return

    item = session["selected_item"] or {}

    print(
        f"  found:    {item.get('title')} — "
        f"${item.get('price')} on {item.get('platform')}"
    )
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")

    _show(
        run_agent(
            query="looking for a vintage graphic tee under $30",
            wardrobe=get_example_wardrobe(),
        )
    )

    print("\n=== A query it can't ===")

    _show(
        run_agent(
            query="designer ballgown size XXS under $5",
            wardrobe=get_example_wardrobe(),
        )
    )

    print(
        "\nThe second one should stop before the fit card. "
        "If both paths look the same, the branch isn't doing anything yet."
    )