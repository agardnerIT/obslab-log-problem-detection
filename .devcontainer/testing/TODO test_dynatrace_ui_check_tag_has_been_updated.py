from loguru import logger
from helpers import *

TEST_TIMEOUT_SECONDS = os.environ.get("TESTING_TIMEOUT_SECONDS", 60)

@pytest.mark.timeout(TEST_TIMEOUT_SECONDS)
def test_dynatrace_ui(page: Page):

    # It is a classic app
    app_visual_name = "Settings Classic"
    app_name = "settings"

    ################################################
    logger.info("Logging in")
    login(page)

    # ################################################
    logger.info("Opening search menu")
    open_search_menu(page)
    
    
    # ################################################
    logger.info(f"Searching for {app_visual_name}")
    search_for(page, app_visual_name)

    # ################################################
    logger.info(f"Opening {app_visual_name} app")
    open_app_from_search_modal(page, app_name, is_classic_app=True)

    # ################################################
    logger.info(f"{app_name} app is now displayed")

    # Open tags menu
    logger.info("Opening Tags Menu")
    wait_for_app_to_load(page, is_classic_app=True)
    app_frame_locator, app_frame = get_app_frame_and_locator(page, is_classic_app=True)

    # Find and click on "Tags"
    expect(app_frame_locator.get_by_title("Tags", exact=True).first).to_contain_text("Tags", timeout=WAIT_TIMEOUT)
    tags_element = app_frame_locator.get_by_title("Tags", exact=True).first
    tags_element.click()

    # Find and click on "Automatically applied tags"
    automatically_applied_tags_element = app_frame_locator.get_by_title("Automatically applied tags", exact=True).first
    expect(automatically_applied_tags_element).to_contain_text("Automatically applied tags", timeout=WAIT_TIMEOUT)
    automatically_applied_tags_element.click()

    # Open invidual tag dropdown
    tag_name = "crossplane-created"
    tag_description = "this is an autotag rule created by crossplane ABC123"

    app_frame_locator.get_by_role("row", name=tag_name, exact=True).get_by_role("button").click()

    # Wait for correct tag description    
    expect(app_frame_locator.get_by_text(tag_description, exact=True)).to_have_text(tag_description, timeout=WAIT_TIMEOUT)