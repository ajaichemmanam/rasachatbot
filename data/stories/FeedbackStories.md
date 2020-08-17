
## quit
* quit
    - utter_ok
    > check_ask_feedback

## thanks
* thanks
    - utter_noworries
    > check_ask_feedback

## give feedback
> check_ask_feedback
    - feedback_form
    - form{"name": "feedback_form"}
    - slot{"requested_slot": "feedback"}
    - utter_ask_feedback
    - action_listen
* form: affirm
    - feedback_form
    - slot{"feedback": true}
    - slot{"requested_slot": "feedback_reason"}
* form: chitchat
    - form: feedback_form
    - slot{"feedback_reason": "Nothing much. You are good"}
    - form{"name": null}
    - slot{"requested_slot": null}

## deny feedback
> check_ask_feedback
    - feedback_form
    - form{"name": "feedback_form"}
    - slot{"requested_slot": "feedback"}
    - utter_ask_feedback
    - action_listen
* form: deny
    - feedback_form
    - slot{"feedback": false}
    - form{"name": null}
    - slot{"feedback": null}
    - slot{"requested_slot": null}

## feedback explained
> check_asked_feedback
 - feedback_form
    - form{"name": "feedback_form"}
    - slot{"requested_slot": "feedback"}
    - utter_ask_feedback
    - action_listen
* explain
  - utter_explain_why_feedback
  - utter_ask_feedback
  > check_asked_feedback

<!-- 
## user allows feedback
> check_asked_feedback
* affirm
  - form: feedback_form
  - slot{"requested_slot": "feedback_reason"}
  - form{"name": null}

## user denies feedback
> check_asked_feedback
* deny
  - utter_ok
  - form{"name": null} -->
