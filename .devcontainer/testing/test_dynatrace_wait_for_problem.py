from loguru import logger
from helpers import *
import time

TEST_TIMEOUT_SECONDS = os.environ.get("TESTING_TIMEOUT_SECONDS", 60)
SLEEP_TIME_BETWEEN_PROBLEM_LOOKUP_ATTEMPTS = os.environ.get("TESTING_SLEEP_TIME_BETWEEN_PROBLEM_LOOKUP_ATTEMPTS", 30)

@pytest.mark.timeout(TEST_TIMEOUT_SECONDS)
def test_dynatrace_ui(page: Page):

    app_visual_name = "Notebooks"
    app_name = "notebooks"

    ################################################
    logger.info("Logging in")
    login(page)

    # Open the notebooks app
    app_visual_name = "Notebooks"
    app_name = "notebooks"

    logger.info("Opening search menu")
    open_search_menu(page)

    # ################################################
    logger.info(f"Searching for {app_visual_name}")
    search_for(page, app_visual_name)

    logger.info(f"Opening {app_visual_name} app")
    open_app_from_search_modal(page, app_name, is_classic_app=False)

    # ################################################
    logger.info(f"{app_name} app is now displayed")

    time.sleep(5)

    create_new_document(page=page, close_microguide=True)
    add_document_section(page=page, section_type_text=SECTION_TYPE_DQL)
    # Deliberately do not validate using hte built-in logic here
    # Because it is likely that problem record does not exist first time around
    enter_dql_query(page=page, dql_query=retrieve_dql_query("fetch problems with dql"), section_index=0, validate=False)

    # Search for problem 
    wait_for_app_to_load(page)
    app_frame_locator, app_frame = get_app_frame_and_locator(page)
    count = 0
    DATA_FOUND = False
    while count < 10:
        # Run the DQL query and see if a problem exists or not
        # Click the Run button
        section = app_frame_locator.locator("[data-testid-section-index=\"0\"]")
        section.get_by_test_id("run-query-button").click(timeout=WAIT_TIMEOUT)

        # wait for DQL to finish
        # if this times out, either query took too long
        # of the query was invalid
        try:
            section.get_by_test_id("result-container").wait_for(timeout=WAIT_TIMEOUT)
        except:
            pytest.fail("Either query timed out or an invalid query was provided.")

        # Try to find the "no data" <h6>
        # In this case, this is expected for most of this loop
        # The logic here is to find this, sleep, increment the counter then try again
        # If indeed data IS found, break out of the loop 
        no_data_heading = section.locator("h6")
        if not no_data_heading.is_visible():
            DATA_FOUND = True
            break
        else:
            # Sleep for 30s between attempts
            time.sleep(SLEEP_TIME_BETWEEN_PROBLEM_LOOKUP_ATTEMPTS)
            count += 1

    if not DATA_FOUND:
        pytest.fail(f"No data found, despite polling for {count*SLEEP_TIME_BETWEEN_PROBLEM_LOOKUP_ATTEMPTS} seconds")

    delete_document(page=page)