window.onload = function () {
    // reference to the REDIPS.drag class
    var rd = REDIPS.drag;
    // initialization
    rd.init();
    toggle_dragging(true);
}
// toggles trash_ask parameter defined at the top
function toggle_confirm(chk) {
    REDIPS.drag.trash_ask = chk.checked;
}

// enables / disables dragging
function toggle_dragging(flag) {
    REDIPS.drag.enable_drag(flag);
}

// show prepared content for saving
function save(){
    // scan first table
    var content = REDIPS.drag.save_content();
    // if content doesn't exist
    if (content === '') {
        alert('Table is empty!');
    }
    else {


        $.post( "/post_desired_schedule", {
            'javascript_data': JSON.stringify(content)
        });

        toggle_dragging(false);
    }
}
