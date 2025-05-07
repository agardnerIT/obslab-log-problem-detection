from loguru import logger
from helpers import *
import time

TEST_TIMEOUT_SECONDS = os.environ.get("TESTING_TIMEOUT_SECONDS", 60)

@pytest.mark.timeout(TEST_TIMEOUT_SECONDS)
def test_dynatrace_ui(page: Page):

    app_visual_name = "Logs"
    app_name = "logs"

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
    open_app_from_search_modal(page, app_name, is_classic_app=False)

    # ################################################
    logger.info(f"{app_name} app is now displayed")

    # Open logs menu
    wait_for_app_to_load(page, is_classic_app=False)
    app_frame_locator, app_frame = get_app_frame_and_locator(page, is_classic_app=False)

    # Find and click on "Logs DQL Builder" search box
    logs_search_box = app_frame_locator.get_by_label("Filter field")
    #logs_search_box = app_frame_locator.get_by_test_id("dqlbuiler-form-field")
    logger.info(logs_search_box)
    #expect(logs_search_box).to_be_attached(timeout=WAIT_TIMEOUT)
    expect(logs_search_box).to_be_editable(timeout=WAIT_TIMEOUT)
    logs_search_box.click(timeout=WAIT_TIMEOUT)
    time.sleep(1)
    logs_search_box.type(text="service.name=cart", delay=50)

    search_button = app_frame_locator.get_by_test_id("logs-input-container__run-query")
    search_button.click(timeout=WAIT_TIMEOUT)
    
    # Wait for search results
    log_table = app_frame_locator.get_by_test_id("logs-table-search")
    expect(log_table).to_be_visible(timeout=WAIT_TIMEOUT)

    time.sleep(5)

    # Open services screen
    app_visual_name = "Services"
    app_name = "services"

    logger.info("Opening search menu")
    open_search_menu(page)

    # ################################################
    logger.info(f"Searching for {app_visual_name}")
    search_for(page, app_visual_name)

    logger.info(f"Opening {app_visual_name} app")
    open_app_from_search_modal(page, app_name, is_classic_app=False)

    # ################################################
    logger.info(f"{app_name} app is now displayed")

    # Open services list
    expect(app_frame_locator.get_by_test_id("resource-health-card-surface").first).to_be_attached(timeout=WAIT_TIMEOUT)
    services_list_box = app_frame_locator.get_by_test_id("resource-health-card-surface").first
    expect(services_list_box).to_be_visible(timeout=WAIT_TIMEOUT)
    services_list_box.click()

    # Wait for services app to load
    services_header = app_frame_locator.get_by_test_id("dql-table-header")
    expect(services_header).to_have_text("Services", timeout=WAIT_TIMEOUT)

    cart_service_hyperlink = app_frame_locator.get_by_test_id("entity-details-button").get_by_text("cart")
    expect(cart_service_hyperlink).to_be_attached(timeout=WAIT_TIMEOUT)
    cart_service_hyperlink.click()

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
    enter_dql_query(page=page, dql_query=retrieve_dql_query("fetch cart service logs"), section_index=0, validate=True)
    delete_document(page=page)