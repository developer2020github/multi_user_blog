/*

this mddule implements delete with confirmation logic
On page load follwing buttons are shown 

"edit submit form" "delete"


if user clicks edit submit form button - edited post will be submitted normal way 
(cou;d implement a preview, but user can always go back to edit)

if user clicks delete button, following buttons will be shown:
  "go back" "delete confrim (form submit)""
  edit submit form and delete get hidden

if user clicks "go back ":
 "edit submit form" , "delete" buttons will be shown again
 
if user clicks "delete cofirm" - delete form will be submited


*/


var delete_confirm_button;
var go_back_button;
var edit_submit_button;
var unconfirmed_delete_button;
var cancel_edits_button;


function unconfirmed_delete_button_click() {

    unconfirmed_delete_button.style.display = "none";
    edit_submit_button.style.display = "none";
    cancel_edits_button.style.display = "none";
    delete_confirm_button.style.display = "inline-block";
    go_back_button.style.display = "inline-block";
}

function go_back_button_click() {

    unconfirmed_delete_button.style.display = "inline-block";
    edit_submit_button.style.display = "inline-block";
    delete_confirm_button.style.display = "none";
    go_back_button.style.display = "none";
    cancel_edits_button.style.display = "inline-block";
}

function assign_buttons() {

    delete_confirm_button = document.getElementById("delete-post-confirm-submit-button");
    go_back_button = document.getElementById("back-to-edit-delete-page-button");
    edit_submit_button = document.getElementById("edit-post-submit-form-button");
    unconfirmed_delete_button = document.getElementById("delete-post-button");
    cancel_edits_button  = document.getElementById("cancel-edits-button");
}

function assign_click_events() {

    unconfirmed_delete_button.addEventListener("click", unconfirmed_delete_button_click);
    go_back_button.addEventListener("click", go_back_button_click);
}

document.addEventListener('DOMContentLoaded', function() {
	
    assign_buttons();
    assign_click_events();
}, false);
