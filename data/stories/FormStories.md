## form all details given when prompted
* greet
    - utter_greet
    - utter_help
* travel{"location": "afghanistan"}
    - slot{"location": "afghanistan"}
    - bio_form
    - form{"name": "bio_form"}
    - slot{"requested_slot": "name"}
* form: inform{"name": "ajai"}
    - slot{"name": "ajai"}
    - bio_form
    - slot{"name": "ajai"}
    - slot{"requested_slot": "age"}
* form: inform{"age": "23"}
    - slot{"age": "23"}
    - bio_form
    - slot{"age": "23"}
    - slot{"requested_slot": "email"}
* form: inform{"email": "ajaichemmanam@gmail.com"}
    - slot{"email": "ajaichemmanam@gmail.com"}
    - form: bio_form
    - slot{"email": "ajaichemmanam@gmail.com"}
    - slot{"requested_slot": "address"}
* form: inform{"address": "2nd cross, bangalore, India"}
    - slot{"address": "2nd cross, bangalore, India"}
    - form: bio_form
    - slot{"address": "2nd cross, bangalore, India"}
    - form{"name": null}
    - slot{"requested_slot": null}
* affirm
    - utter_ok


## form explained all slots
* greet
    - utter_greet
    - utter_help
* travel{"location": "afghanistan"}
    - slot{"location": "afghanistan"}
    - bio_form
    - form{"name": "bio_form"}
    - slot{"requested_slot": "name"}
* explain
    - utter_explain_why_name
    - utter_ask_name
    - action_listen
* form: inform{"name": "ajai"}
    - slot{"name": "ajai"}
    - bio_form
    - slot{"name": "ajai"}
    - slot{"requested_slot": "age"}
* explain
    - utter_explain_why_age
    - utter_ask_age
    - action_listen
* form: inform{"age": "23"}
    - slot{"age": "23"}
    - bio_form
    - slot{"age": "23"}
    - slot{"requested_slot": "email"}
  * explain
    - utter_explain_why_email
    - utter_ask_email
    - action_listen
* form: inform{"email": "ajaichemmanam@gmail.com"}
    - slot{"email": "ajaichemmanam@gmail.com"}
    - form: bio_form
    - slot{"email": "ajaichemmanam@gmail.com"}
    - slot{"requested_slot": "address"}
* form: inform{"address": "1st street, Mumbai, India"}
    - slot{"address": "1st street, Mumbai, India"}
    - form: bio_form
    - slot{"address": "1st street, Mumbai, India"}
    - form{"name": null}
    - slot{"requested_slot": null}
* affirm
    - utter_ok

## form explain age 
* greet
    - utter_greet
    - utter_help
* travel{"location": "afghanistan"}
    - slot{"location": "afghanistan"}
    - bio_form
    - form{"name": "bio_form"}
    - slot{"requested_slot": "name"}
* form: inform{"name": "ajai"}
    - slot{"name": "ajai"}
    - bio_form
    - slot{"name": "ajai"}
    - slot{"requested_slot": "age"}
* explain
    - utter_explain_why_age
    - utter_ask_age
    - action_listen
* form: inform{"age": "23"}
    - slot{"age": "23"}
    - bio_form
    - slot{"age": "23"}
    - slot{"requested_slot": "email"}
* form: inform{"email": "ajaichemmanam@gmail.com"}
    - slot{"email": "ajaichemmanam@gmail.com"}
    - form: bio_form
    - slot{"email": "ajaichemmanam@gmail.com"}
    - slot{"requested_slot": "address"}
* form: inform{"address": "2nd cross, bangalore, India"}
    - slot{"address": "2nd cross, bangalore, India"}
    - form: bio_form
    - slot{"address": "2nd cross, bangalore, India"}
    - form{"name": null}
    - slot{"requested_slot": null}
* affirm
    - utter_ok