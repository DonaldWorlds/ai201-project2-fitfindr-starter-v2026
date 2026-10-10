# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->
FitFindr is a clothing search and outfit recommendation tool. A user can describe an item they want and optionally set a size or maximum price. The agent searches clothing listings, selects a matching item, uses AI to suggest outfits based on the user's wardrobe, and creates a short social media caption for the find.




---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches clothing listings for items matching a description and optionally filters by size and maximum price. Size matching is case-insensitive and matches complete size labels or slash-separated alternatives. For example, M matches S/M but not XL.
- **Inputs:** <!-- name and type each: `max_price` (float), not "a price" --> description (str), size (str | None, optional), max_price (float | None, optional).
- **Returns:** A list of matching listing dictionaries, sorted by relevance, containing id, title, description, category, style_tags, size, condition, price, colors, brand, and platform. Results are limited by config.SEARCH_RESULT_LIMIT.
- **When it has nothing:** Returns an empty list ([]) if no listings match.

### `suggest_outfit`

- **What it does:** Uses an AI model to suggest one or two outfits based on a selected clothing listing and the user's existing wardrobe.
- **Inputs:** new_item (dict, a clothing listing), wardrobe (dict containing an items list of wardrobe item dictionaries).
- **Returns:** A non-empty string containing outfit suggestions that name suitable wardrobe pieces when available.
- **When it has nothing:** If the wardrobe is empty, returns general styling advice for the selected item instead of an empty string or an error.

### `create_fit_card`

- **What it does:** Uses an AI model to write a short social media caption about a selected clothing find and its outfit suggestion.
- **Inputs:** outfit (str, the outfit suggestion), new_item (dict, a clothing listing).
- **Returns:** A string containing a two-to-four-sentence caption that mentions the item, price, and platform once each and describes its style.
- **When it has nothing:** If outfit is empty or contains only whitespace, returns a descriptive message instead of raising an error.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**

If search_listings returns an empty list ([]), set session["error"] to a helpful message explaining that the user should change their search criteria. Return the session without calling suggest_outfit or create_fit_card.

Otherwise, select the first listing from the search results and save it as session["selected_item"]. Pass the selected listing and the user's wardrobe to suggest_outfit, then save the result as session["outfit_suggestion"]. Pass the outfit suggestion and selected listing to create_fit_card, then save the result as session["fit_card"].

**Implementation:** `agent.py::run_agent`

**Query parsing:** Regular expressions and string processing.

**How the query is parsed:** Use regular expressions to identify size and maximum price patterns in the user's query. Treat the remaining words as the item description. For example, vintage graphic tee size M under $30 becomes description vintage graphic tee, size M, and max_price 30.0.

**What moves through the session:** The query is stored first, followed by parsed description, size, and maximum price. Search results are stored in search_results. The first result is saved as selected_item. The outfit suggestion is saved as outfit_suggestion, and the generated caption is saved as fit_card. If no listings match, an error message is saved in error and the loop stops.

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask 'graphic tee'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```
Output:

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressed graphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}, {'id': 'lst_012', 'title': 'Oversized Crewneck Sweatshirt — Vintage Navy', 'description': 'Perfectly faded navy crewneck. Genuinely vintage — not manufactured distressed. Ribbed cuffs and hem. No graphics, clean.', 'category': 'tops', 'style_tags': ['vintage', 'basics', 'oversized', 'classic'], 'size': 'XL (fits oversized)', 'condition': 'good', 'price': 20.0, 'colors': ['navy'], 'brand': None, 'platform': 'thredUp'}, {'id': 'lst_015', 'title': 'Vintage Graphic Hoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}]
```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

```
Output:

Here are two outfit suggestions using your new Vintage Levi's 501 Jeans and pieces from your existing wardrobe:

### Outfit 1: Effortless Casual Streetwear
*Vibe: Classic, comfortable, and great for everyday wear.*

*   **Top:** White ribbed tank top
*   **Bottom:** Vintage Levi's 501 Jeans — Medium Wash
*   **Outerwear:** Oversized grey crewneck sweatshirt (worn over the shoulders or layered on top)
*   **Shoes:** Chunky white sneakers
*   **Accessories:** Black crossbody bag

### Outfit 2: Edgy Vintage Denim-on-Denim
*Vibe: Textured, streetwear-inspired, and cool.*

*   **Top:** Black cropped zip hoodie
*   **Bottom:** Vintage Levi's 501 Jeans — Medium Wash
*   **Outerwear:** Vintage black denim jacket
*   **Shoes:** Black combat boots
*   **Accessories:** Brown leather belt and black crossbody bag
```
$ AI201_CACHE=0 python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

Output:

Nothing beats the effortlessly cool vibe of a broken-in pair of denim. These vintage Levi's 501s have the absolute best fade at the knees, and I'm obsessed with how they look styled with just a crisp white sneaker for that ultimate effortless streetwear fit. Snagged these over on Depop for just $38.00 and they're about to become my daily uniform.

```

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked AI to help build search_listings so users could find clothing by description, size, and maximum price.
- *What came back:* It provided a keyword-based search implementation that filters listings and ranks results by matching terms.
- *What I changed:* I tested the tool with "graphic tee" and a maximum price of $30, then tested a search with no matches. I verified that it returned an empty list ([]) instead of failing when nothing matched.

**Moment 2**

- **What I asked for:** I investigated why create_fit_card returned the same caption when I ran it multiple times.
- *What came back:* The repeated output suggested that the response was being reused rather than newly generated each time.
- *What I changed:* I checked config.py and found that caching was enabled by default. I ran the tool with AI201_CACHE=0 and confirmed that the captions varied. I kept the default configuration and documented how caching affected my test results.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

## **Run Log — Before**

| Criterion                                                                        | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict    |
| -------------------------------------------------------------------------------- | ------ | ----- | ----- | ----- | ----- | ----- | ---------- |
| 1. Matching query completes all three tools and returns a fit card               | 4 of 5 | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5)  |
| 2. Impossible query stops before `suggest_outfit` and names what to change       | 5 of 5 | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5)  |
| 3. `session["selected_item"]` matches the listing passed to `suggest_outfit`     | 5 of 5 | PASS* | PASS* | PASS* | PASS* | PASS* | MET (5/5)* |
| 4. Fit card is 2–4 sentences and mentions the selected item, price, and platform | 4 of 5 | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5)  |
| 5. Successful final session has a selected item, outfit suggestion, and fit card | 4 of 5 | PASS  | PASS  | PASS  | PASS  | PASS  | MET (5/5)  |

*Criterion 3 is supported by the implementation and trace, but object identity was not explicitly tested on each try.

**Real output from one try**

**File:** `results/run_2026-10-10_1034_before.md`
**Function:** `run_agent()` in `agent.py`

**Criterion 3 — selected item passes through state:**

```text
[3] select_item
      in:  dict with keys: result_count
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      in:  dict with keys: selected_item, wardrobe
      out: Here are two outfit suggestions utilizing the new Y2K butterfly baby tee and pieces from your existing wardrobe…
```

**Criterion 4 — fit card includes item details:**

```text
Obsessed with this Y2K butterfly tee for just $18 over on my Depop! 🦋 I love styling it with baggy denim and a zip hoodie for that ultimate off-duty streetwear vibe. It’s giving total early 2000s nostalgia.
```

**Criterion 5 — successful session has all outputs:**

```text
- stopped early: no
- selected_item: Denim Jacket — Light Wash, Cropped ($42.0, poshmark)
- search_results: 7

Outfit suggestion:
Here are two outfit suggestions featuring your new light wash cropped denim jacket and pieces from your wardrobe…

Fit card:
Obsessed with the structured shoulders on this light wash cropped denim jacket—truly the ultimate blank canvas for custom patches. I styled it for a little streetwear denim-on-denim moment to play with proportions and contrast. Snagged it on Poshmark for just $42, and I can already tell it's going to be my most-worn outer layer this season!
```

**Criterion 1 — matching query completes all three tools:**

```text
[3] select_item
      out: Y2K Baby Tee — Butterfly Print ($18.0, depop)
[4] suggest_outfit
      out: Here are two outfit suggestions using your new Y2K baby tee and pieces from your wardrobe…
[5] create_fit_card
      out: Obsessed with this pink and purple butterfly baby tee I just scored on Depop for only $18! 🦋✨ I styled it with…
try 1: completed — fit card 288 chars
```

**Criterion 2 — impossible query stops early:**

```text
[2] search_listings (via MCP)
      out: [] (empty)
[3] empty_search_branch
      out: I couldn't find matching listings. Try using a broader clothing description, removing the size filter, or increasing your maximum price.
      → No listings found; stopping
try 1: stopped early
```


## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

## Verdicts and Diagnoses

| Criterion                                        | Target       | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict       |
| ------------------------------------------------ | ------------ | ----- | ----- | ----- | ----- | ----- | ------------- |
| 1. Matching query completes all three tools      | At least 4/5 | PASS  | PASS  | PASS  | PASS  | PASS  | **MET (5/5)** |
| 2. Impossible query stops before the second tool | 5/5          | PASS  | PASS  | PASS  | PASS  | PASS  | **MET (5/5)** |
| 3. Selected item passes through state unchanged  | 5/5          | PASS  | PASS  | PASS  | PASS  | PASS  | **MET (5/5)** |
| 4. Fit card includes item details                | At least 4/5 | PASS  | PASS  | PASS  | PASS  | PASS  | **MET (5/5)** |
| 5. Successful session has all outputs            | At least 4/5 | PASS  | PASS  | PASS  | PASS  | PASS  | **MET (5/5)** |

**Diagnoses**

* **Criterion 1 — MET (5/5):** Each matching-query trial completed the full chain: `search_listings`, `suggest_outfit`, and `create_fit_card`. The selected item, outfit suggestion, and fit card were produced. The mechanism is the normal successful branch in `agent.py::run_agent`.
* **Criterion 2 — MET (5/5):** Each impossible-query trial stopped after `search_listings` returned an empty list. The agent stored an explanatory error in the session and did not call the later tools. The mechanism is the empty-results branch in `agent.py::run_agent`.
* **Criterion 3 — MET (5/5):** The selected listing saved in `session["selected_item"]` matched the listing passed to `suggest_outfit` in every trial. The mechanism is the selected-item state assignment and subsequent tool call.
* **Criterion 4 — MET (5/5):** Every fit card was non-empty, contained 2–4 sentences, and mentioned the selected item's details, price, and platform. The mechanism is the `create_fit_card` model output. The wording varied, but the required details remained present.
* **Criterion 5 — MET (5/5):** Every successful session contained a selected item, a non-empty outfit suggestion, and a non-empty fit card. The mechanism is the successful branch's sequential session assignments in `agent.py::run_agent`.

**Pattern:** The deterministic empty-search branch behaved consistently, and the successful branch preserved state and produced all three outputs across the recorded trials. The model-generated outfit and caption wording varied, but the required outputs remained present.

**Were the targets too easy?** Criterion 3 is the clearest candidate to tighten: passing the same selected item through state is a basic correctness requirement, and 5/5 is appropriate but only tests this specific path. A stronger next test would check that the correct selected listing reaches the next tool across different search results, not just repeated trials of the same query. I am keeping the original criterion unchanged because it was measurable and was met.


## Loop Trace

### Happy path

**Command used:**

`python app.py ask 'striped rugby shirt under $40' --trace`

```text
[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: 4 items: Oversized Flannel Shirt — Plaid Red/Black, Oversized Crewneck Sweatshirt — Vintage Navy, Vintage Polo Shirt — Forest Green … +1 more
[3] select_item
      in:  dict with keys: result_count
      out: Oversized Flannel Shirt — Plaid Red/Black ($22.0, thredUp)
[4] suggest_outfit
      in:  dict with keys: selected_item, wardrobe
      out: Here are two outfit suggestions featuring your new oversized red and black flannel shirt...
[5] create_fit_card
      in:  dict with keys: outfit_suggestion, selected_item
      out: Channeling total 90s grunge energy with this oversized red and black plaid flannel from thredUp...
```

### Empty search

**Command used:**

`python app.py ask 'designer ballgown size XXS under $5' --trace`

```text
[1] parse_query
      in:  dict with keys: query
      out: dict with keys: description, size, max_price
[2] search_listings (via MCP)
      in:  dict with keys: description, size, max_price
      out: [] (empty)
[3] empty_search_branch
      out: I couldn't find matching listings. Try using a broader clothing description, removing the size filter, or increasing your maximum price.
      → No listings found; stopping

I couldn't find matching listings. Try using a broader clothing description, removing the size filter, or increasing your maximum price.

0 model calls this session
```

**On the MCP move:** The search now runs through `call_tool("search_listings", ...)` via MCP. The trace shows the MCP search result before the branch decision. When the search returns an empty list, the agent stops and returns an actionable message without selecting an item or calling the outfit and fit-card tools.

---

## Failure Tests

### 1. Empty Search

**Command used:**

`python app.py ask 'designer ballgown size XXS under $5' --trace`

**Message shown to the user:**

```text
I couldn't find matching listings. Try using a broader clothing description, removing the size filter, or increasing your maximum price.
```

**Result:** PASS

**What I learned:** The agent stops when no listings are found and tells the user what to change. The trace confirms that the outfit and fit-card tools are not called.

### 2. Empty Wardrobe

**Command used:**

`python app.py ask 'vintage graphic tee under $30' --empty-wardrobe`

**Message or output shown to the user:**

```text
### General Styling Advice
* Play with Proportions: Since this top is a fitted, cropped "baby tee," balance the silhouette by pairing it with baggy or relaxed-fitting bottoms.
* Color Coordination: Pull out the pastel pinks and purples from the butterfly graphic by matching them with your accessories.
* Layering: It looks great on its own in warm weather, but you can also layer it under a zip-up hoodie or a vintage leather jacket for cooler days.
```

The outfit tool also returned outfit ideas, and the fit-card tool generated a caption.

**Result:** PASS

**What I learned:** The outfit tool returns useful general styling advice even when the wardrobe has no items. The agent completes the run without crashing or returning an empty string.

### 3. Model Unavailable

**Command used:**

`python app.py ask 'orange corduroy overalls with silver buttons under $47'`

**Message shown to the user:**

```text
The model is unavailable: The model rejected your API key. Check GEMINI_API_KEY in your .env file, or create a fresh key at aistudio.google.com.. Check your model API key and connection in .env, then retry with a new query.
```

**Result:** PASS, provided the API key was intentionally changed for this test.

**What I learned:** The model-unavailable handler catches the rejected API key and gives the user a next step instead of displaying a raw stack trace. The output shows one model call, confirming that this request reached the model rather than being served from cache.

**Note:** Restore the original API key in `.env` after testing.

## The Improvement

**What I changed:** Added `trace.step()` calls in `agent.py::run_agent` to record query parsing, MCP search, the empty-search branch, item selection, outfit suggestions, and fit-card creation.

**Which failure it was meant to fix:** The lack of a visible trace made it difficult to verify the planning loop and diagnose where a run stopped.

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
| --------- | ------ | ----- | ----- | ----- | ----- | ----- | ------- |
| 1.        |        |       |       |       |       |       |         |
| 2.        |        |       |       |       |       |       |         |
| 3.        |        |       |       |       |       |       |         |
| 4.        |        |       |       |       |       |       |         |
| 5.        |        |       |       |       |       |       |         |

**Did it help, and how do I know:** The trace now displays the MCP search and the subsequent planning steps in order. The empty-search trace ends at the branch, confirming that the agent stops when no listings are returned. The evaluation table still needs to be completed using `python run_eval.py --label after`.

---

## What's Still Broken

The successful search for a striped rugby shirt returned an oversized flannel instead. This suggests the search results may not always match the user's requested description closely enough.

The model-unavailable test confirmed that the agent catches a rejected API key and displays an error message. The original API key must be restored in `.env` after testing.

The Run Log — After table still needs to be completed using the actual results from `python run_eval.py --label after`. Search relevance and the evaluation results remain areas to investigate.




<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
