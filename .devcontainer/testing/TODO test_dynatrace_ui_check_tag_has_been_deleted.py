from loguru import logger
from helpers import *
import time

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

    # Expect tag NOT to exist
    # loc = app_frame_locator.locator(f"dtx-markdown[uitestid=\"cell-summary\"] div.content:has-text(\"{tag_name}\")")
    # loc = app_frame.locator(f"dtx-markdown[uitestid=\"cell-summary\"]")
    # Locate the outer iframe
    #outer_frame = app_frame_locator

    # Quite honestly, I have no idea why this first line
    # is necessary, but 4 days into this and this is the only reliable way I can find to make this work.
    # I can't waste any more time on this, so this will do
    FOUND_ITEM = True
    try:
        page.locator("[data-testid=\"cluster-wrapper-app-iframe\"]").content_frame.get_by_text(tag_name, exact=True).wait_for(timeout=WAIT_TIMEOUT)
    except Exception as te:
        FOUND_ITEM = False
        logger.info(f"Tried waiting for {tag_name} and couldn't find it (this is a good thing)")

    expect(page.locator("[data-testid=\"cluster-wrapper-app-iframe\"]").content_frame.get_by_text(tag_name, exact=True)).not_to_be_visible(timeout=WAIT_TIMEOUT)

    # try:
        
    # except AssertionError as ae:
    #     logger.info(ae)
    #     pytest
    
    # try:
    #     #item = page.locator("[data-testid=\"cluster-wrapper-app-iframe\"]").content_frame.get_by_text(tag_name, exact=True)
    #     #logger.info(f"Item Count: {item.count()}. Text Content: {item.text_content()}")
    #     #time.sleep(5)
    #     # Quite honestly, I have no idea why this first line
    #     # is necessary, but 4 days into this and this is the only reliable way I can find to make this work.
    #     # I can't waste any more time on this, so this will do
    #     page.locator("[data-testid=\"cluster-wrapper-app-iframe\"]").content_frame.get_by_text(tag_name, exact=True).wait_for(timeout=WAIT_TIMEOUT)
    #     expect(page.locator("[data-testid=\"cluster-wrapper-app-iframe\"]").content_frame.get_by_text(tag_name, exact=True)).not_to_be_visible(timeout=WAIT_TIMEOUT)
    #     #page.locator("[data-testid=\"cluster-wrapper-app-iframe\"]").content_frame.get_by_role("row", name="crossplane-created2").get_by_role("button").click()
    #     #page.locator("[data-testid=\"cluster-wrapper-app-iframe\"]").content_frame.get_by_role("row", name="crossplane-created2 Show").locator("dt-expandable-cell").get_by_role("button").click()
    #     # page.locator("[data-testid=\"cluster-wrapper-app-iframe\"]").content_frame.get_by_role("row", name="crossplane-created", exact=True).get_by_role("button").click()
    #     # page.locator("[data-testid=\"cluster-wrapper-app-iframe\"]").content_frame.locator("form-readonly").filter(has_text="crossplane-created2").dblclick()
    #     # time.sleep(2)
    #     #loc = app_frame_locator.locator('[uitestid="cell-summary"]').get_by_text(tag_name)
    #     #loc = app_frame_locator.get_by_role("row", name=tag_name, exact=True)
    #     #logger.info(loc.all())
    #     #logger.info(loc.all_inner_texts())
    #     #logger.info(loc.all_text_contents())
    # except Exception as e:
    #     logger.info(e)
    #     logger.info("Could not find element (this is a good thing).")
    # finally:
    #     logger.info("Test completed. Tag removed.")
        
    
    # page.frame_locator('//div//dtx-markdown')
    # loc = app_frame_locator.locator('//div//dtx-markdown')
    
    # #loc = app_frame_locator.get_by_text("crossplane-created")
    # #frame_loc = page.frame_locator("div")
    # #frame_loc.
    # #loc = outer_frame.locator('dtx-markdown[uitestid="cell-summary"]')
    # #loc = outer_frame.locator('div')
    # #frame_loc.get
    # #frame_loc.a

    # #logger.info(outer_frame)
    # logger.info("HERE #1")
    # logger.info(loc.all())
    # logger.info("HERE #2")

    # # Locate the inner iframe within the outer iframe
    # #inner_frame = outer_frame.frame_locator('#app-iframe')

    # # Wait for the <div> element containing the text "crossplane-created" to be present
    # #inner_frame.locator('dtx-markdown[uitestid="cell-summary"] div.content:has-text("crossplane-created")').wait_for(state='visible')
    # #loc = inner_frame.locator('dtx-markdown[uitestid="cell-summary"]')
    # #loc.all()

    
    # #loc = app_frame_locator.frame_locator("dtx-markdown[uitestid=\"cell-summary\"]").
    # logger.info(loc.all())
    # if len(loc.all()) == 0:
    #     logger.info(f"Could not find {tag_name} (this is a good thing)")
    # else:
    #     logger.error(f"{tag_name} was found (not good). Error")
    #     pytest.fail(reason=f"{tag_name} WAS found (and shouldn't have been)")
    #expect(app_frame_locator.locator(f"dtx-markdown[uitestid=\"cell-summary\"] div.content:has-text(\"{tag_name}\")")).not_to_have_text(tag_name, timeout=WAIT_TIMEOUT)
