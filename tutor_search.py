import pandas as pd
from rapidfuzz import process, fuzz


def tutor_search(dfs, tutors, tname):

    query = str(tname).strip()

    # First try an exact match.
    exact_match = next(
        (
            str(tutor).strip()
            for tutor in tutors
            if pd.notna(tutor)
            and str(tutor).strip().casefold() == query.casefold()
        ),
        None
    )

    if exact_match is not None:
        candidate_names = [exact_match]

    else:
        # Fall back to fuzzy matching for approximate searches.
        results = process.extract(
            query,
            tutors,
            scorer=fuzz.WRatio,
            processor=lambda x: str(x).strip().casefold(),
            limit=5,
            score_cutoff=65
        )

        candidate_names = [name for name, score, index in results]

    for name in candidate_names:

        for df in dfs:

            if "Tutor Name" not in df.columns:
                continue

            # Normalize both sides before comparing.
            tutor_column = (
                df["Tutor Name"]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.casefold()
            )

            tutor_details = df[
                tutor_column == str(name).strip().casefold()
            ]

            if not tutor_details.empty:

                print(f"Matched tutor: {name}")
                print(f"Ward records found: {len(tutor_details)}")

                return tutor_details[
                    ["Name", "Registration No"]
                ]

    print(f"No matching tutor found for: {query}")

    return pd.DataFrame(columns=["Name", "Registration No"])