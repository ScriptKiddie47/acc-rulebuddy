# acc-rulebuddy


### Run Locally

1. Install Python Latest Version
1. Check Installation using Command

    ```ps
    $ python -V
    Python 3.13.2
    ```

1. Pull Dependencies ( Pull the same `pypi`)

    ```ps
    conda install conda-forge::python-dotenv
    conda install conda-forge::langchain-openai
    conda install conda-forge::langchain
    conda install conda-forge::fastapi
    conda install conda-forge::uvicorn
    ```
1. Request : 

    ```ps
    curl --request POST \
    --url http://127.0.0.1:8000/rulehelp \
    --header 'content-type: application/json' \
    --data '{
    "user_request": "Why is the rule E101 triggered on my policy 9881923218"
    }'
    ```
1. Response is currently in `content-type : text/plain; charset=utf-8`. But its actually in Markdown.

    ```txt
    **Reason Why Rule E101 is Triggered:**

    The rule `E101` is triggered because it detects a vehicle with specific coverage details that violate the rule's criteria. Specifically, your policy includes a vehicle with the following characteristics:

    - State code: **PA**
    - Bureau vehicle class ID: **LTRK**
    - Vehicle group type: **TTT**

    The rule's logic states that if a vehicle's coverage has:

    - A **state code** that is **not "CA"**,
    - And the **bureau vehicle class ID** is **"LTRK"**,
    - And the **vehicle group type** is **"TIL"**,

    then the rule is violated and triggers an error.

    In your policy data, the vehicle has:

    - `stateCode`: **PA** (not "CA")
    - `bureauVehicleClassIdCd`: **LTRK**
    - `vehicleGroupTypeCd`: **TTT**

    **Since your vehicle's group type is "TTT" (not "TIL"), it does not exactly match the "TIL" specified in the rule.**

    **Possible explanations for triggering:**

    - The rule may have a typo or may refer to a different "vehicle group type" (e.g., "TIL") that is not in your current data.
    - Or, systems may assume "TTT" as equivalent or similar, but the actual rule expects "TIL".

    **Criteria for Rule E101:**

    - Vehicles with `bureauVehicleClassIdCd` as **"LTRK"**,
    - in states other than **"CA"**,
    - with a `vehicleGroupTypeCd` exactly **"TIL"**.

    **Data You Can Change to Avoid Triggering the Rule:**

    1. **Change the vehicle's state code** from **"PA"** to **"CA"**, if appropriate and compliant with your policy.
    2. **Change the vehicle group type** from **"TTT"** to **"TIL"** in your policy data.
    3. **Ensure the coverage details align** with the rule criteria, especially for `vehicleGroupTypeCd`.

    **Summary:**

    - The rule is triggered because the vehicle coverage in your policy does not meet the criteria specified (`vehicleGroupTypeCd` should be "TIL" in non-CA states like PA).
    - To avoid triggering, modify either the **state code** to "CA" or the **vehicle group type** to "TIL".

    Please review your vehicle coverage details accordingly.
    ```
