# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

from rasa_sdk.events import UserUtteranceReverted
from typing import Any, Text, Dict, List, Optional

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet,
    EventType,
    ActionExecuted,
    SessionStarted,
    Restarted,
    FollowupAction,
)
from rasa_sdk import ActionExecutionRejection
from rasa_sdk.forms import FormAction, REQUESTED_SLOT

from actions.actionFunctions import create_mock_profile

# Logging
import logging
logger = logging.getLogger(__name__)
logger.debug("Some log message")  # Use in any function

###################### Form Actions #####################

# Custom Functions
def custom_request_next_slot(
    self,
    dispatcher: "CollectingDispatcher",
    tracker: "Tracker",
    domain: Dict[Text, Any],
) -> Optional[List[EventType]]:
    """Request the next slot and utter template if needed, else return None"""

    for slot in self.required_slots(tracker):
        if self._should_request_slot(tracker, slot):
            logger.debug(f"Request next slot '{slot}'")
            dispatcher.utter_message(
                template=f"utter_ask_{slot}", **tracker.slots
            )
            return [SlotSet(REQUESTED_SLOT, slot)]
     # no more required slots to fill
    return None



# Gather Feedback


class FeedbackForm(FormAction):
    def name(self) -> Text:
        return "feedback_form"

    def request_next_slot(
        self,
        dispatcher: "CollectingDispatcher",
        tracker: "Tracker",
        domain: Dict[Text, Any],
    ) -> Optional[List[EventType]]:

        return custom_request_next_slot(self, dispatcher, tracker, domain)

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        return ["feedback", "feedback_reason"]

    def slot_mappings(self) -> Dict[Text, Any]:
        """A dictionary to map required slots to
            - an extracted entity
            - intent: value pairs
            - a whole message
            or a list of them, where a first match will be picked"""

        return {"feedback": [self.from_intent(intent='affirm',
                                              value=True),
                             self.from_intent(intent='deny',
                                              value=False)],
                "feedback_reason": self.from_text(intent=None)}

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Define what the form has to do
        after all required slots are filled"""
        # Used to get yes or no answer
        feedback = tracker.get_slot("feedback")
        reason = tracker.get_slot("feedback_reason")
        dispatcher.utter_message(
            text="Your feedback was {} due to {}".format(feedback, reason))

        dispatcher.utter_message(
            text="Thanks for your feedback")
        return [SlotSet("feedback", None),
        SlotSet("feedback_reason", None)]
        # return []


class BioForm(FormAction):
    def name(self) -> Text:
        """Unique identifier of the form"""
        return "bio_form"

    @staticmethod
    def required_slots(tracker: Tracker) -> List[Text]:
        """A list of required slots that the form has to fill"""
        # We can use if else statements here
        # if tracker.get_slot('cuisine') == 'greek':
        #     return ["cuisine", "num_people", "outdoor_seating", "preferences", "feedback"]
        # else:
        #     return ["cuisine", "num_people", "preferences", "feedback"]

        return ["name", "age", "email", "address"]

    # Optional
    def slot_mappings(self) -> Dict[Text, Any]:
        return {"name":  self.from_entity(entity="name",
                                          intent='inform'),
                "age": self.from_entity(entity="age",
                                        intent='inform'),
                "email": self.from_entity(entity="email",
                                          intent='inform'),
                "address": self.from_text(intent=None)}

        # Get user input if it matches with the intent "IntentName"
        # "address": self.from_text(intent="IntentName")

        # Used to get yes or no answer
        # [self.from_entity(entity="EntityName"),
        # self.from_intent(intent='affirm',
        #                     value=True),
        # self.from_intent(intent='deny',
        #                     value=False)],

        # Get the value if it matches EntityName from an intent "IntentName"
        # self.from_entity(entity="EntityName",
        #                         intent="IntentName")

        # Get the value if it matches EntityName regardless of intent
        # self.from_entity(entity="EntityName",
        #                         intent=None)

    # Support Functions
    @staticmethod
    def is_int(string: Text) -> bool:
        """Check if a string is an integer"""
        try:
            int(string)
            return True
        except ValueError:
            return False
    '''
    ############### Validate slots individually ###################
    @staticmethod
    def value_db() -> List[Text]:
        """Database of supported slot values"""
        return [
            "caribbean",
            "chinese",
            "french",
            "greek",
            "indian",
            "italian",
            "mexican",
        ]

    def validate_slotname(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
        ) -> Dict[Text, Any]:

        if value.lower() in self.value_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slotname": value}
        else:
            dispatcher.utter_message(text="You gave a wrong input")
            # validation failed, set this slot to None, meaning the user will be asked for the slot again
            return {"slotname": None}
    '''

    
    ############### Validate all slots ###################

    
    def validate(self,
                 dispatcher: CollectingDispatcher,
                 tracker: Tracker,
                 domain: Dict[Text, Any]) -> List[Dict]:

        """Validate extracted requested slot
        else reject the execution of the form action
        """
        # extract other slots that were not requested but set by corresponding entity
        slot_values = self.extract_other_slots(dispatcher, tracker, domain)

        # extract requested slot
        slot_to_fill = tracker.get_slot(REQUESTED_SLOT)
        if slot_to_fill:
            slot_values.update(self.extract_requested_slot(dispatcher,
                                                           tracker, domain))
            if not slot_values:
                #Custom behaviour
                # if slot_to_fill == 'name':
                #     dispatcher.utter_message(text="Sorry. I didn't understand your {} and {}".format(slot_to_fill, slot_values))
                #     return []

                # Normal Behaviour: Raise Action Execution Rejection
                # reject form action execution
                # if some slot was requested but nothing was extracted
                # it will allow other policies to predict another action
                raise ActionExecutionRejection(self.name(),
                                           "Failed to validate slot {0}"
                                           "with action {1}"
                                           "".format(slot_to_fill,
                                                         self.name()))
        # Validate every slots here, and set it to none for that doesn't match
        # for slot, value in slot_values.items():
        #     if slot == 'name':
        #         dispatcher.utter_message(text="Sorry. I didn't understand")
        #         # validation failed, set slot to None
        #         slot_values[slot] = None
        # validation succeed, set the slots values to the extracted values
        return [SlotSet(slot, value) for slot, value in slot_values.items()]
        # return await self.validate_slots(slot_values, dispatcher, tracker, domain)
    

    def submit(self,
               dispatcher: CollectingDispatcher,
               tracker: Tracker,
               domain: Dict[Text, Any]
               ) -> List[Dict]:
        """Define what the form has to do
        after all required slots are filled"""

        # utter submit template
        dispatcher.utter_message(template="utter_bioform_submit")
        # Custom json data in action message 
        # dispatcher.utter_message(text="", json_message={"image_id": "1","payload": "code_1"})

        # Buttons in action message 
        # buttons = []
        # for i in range(3):
        #     buttons.append({"title": "{}".format(str(i)),
        #                     "payload": "my preference is {}".format(str(i))})
        # if len(buttons) == 1:
        #     message = "We found only 1 result"
        # else:
        #     message = "We found multiple results"
        # dispatcher.utter_message(text=message, buttons=buttons)
        return []


# Normal Actions

# Echo user input
class ActionRespondWithUserMessage(Action):
   def name(self):
      return "action_respond_with_user_message"

   def run(self, dispatcher, tracker, domain):
      last_message = tracker.latest_message.get("text", "")
      dispatcher.utter_message(last_message)

      return []

# Reset conversation
class ActionGreetUser(Action):
    """Revertible mapped action for utter_greet"""

    def name(self):
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        dispatcher.utter_message(template="utter_greet")
        return [UserUtteranceReverted()]

# Give sample multimedia messages
class ActionMultimediaExamples(Action):
    """Revertible mapped action for utter_greet"""

    def name(self):
        return "action_multimedia_examples"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        multimedia = tracker.get_slot("multimedia")
        dispatcher.utter_message(template="utter_{}".format(multimedia))
        return []

# Normal Actions
# class ActionHotelSearch(Action):
#     def name(self) -> Text:
#         return "action_hotel_search"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(
#             text="Please wait while I'm looking for a hotel to stay.")
#         location = tracker.get_slot("location")
#         name = tracker.get_slot("name")
#         age = tracker.get_slot("age")
#         address = tracker.get_slot("address")
#         dispatcher.utter_message(
#             text="Shall I book a hotel with following details? {} for 1 person with Name:{}, Age:{} and Address:{}".format(location, name, age, address))
#         return []

# Logic to pass to human


class ActionHumanHandoff(Action):
    def name(self) -> Text:
        return "action_human_handoff"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dispatcher.utter_message(
            text="It looks like you want to be transferred to a human agent")
        dispatcher.utter_message(
            text="Please wait while I'm transferring this chat to our dedicated customer support team")
        dispatcher.utter_message(
            text="Sorry, I Couldn't find a human agent at the moment. Please check back later")
        return []


class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    @staticmethod
    def _slot_set_events_from_tracker(tracker: "Tracker",) -> List["SlotSet"]:
        """Fetch SlotSet events from tracker and carry over keys and values"""

        return [
            SlotSet(key=event.get("name"), value=event.get("value"),)
            for event in tracker.events
            if event.get("event") == "slot"
        ]

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        # the session should begin with a `session_started` event
        events = [SessionStarted()]

        events.extend(self._slot_set_events_from_tracker(tracker))

        # create mock profile
        user_profile = create_mock_profile()

        # initialize slots from mock profile
        for key, value in user_profile.items():
            if value is not None:
                events.append(SlotSet(key=key, value=value))

        # an `action_listen` should be added at the end
        events.append(ActionExecuted("action_listen"))

        return events


class ActionRestart(Action):
    def name(self) -> Text:
        return "action_restart"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[EventType]:

        return [Restarted(), FollowupAction("action_session_start")]
