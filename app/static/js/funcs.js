window.onload = function () {
    // reference to the REDIPS.drag class
    var rd = REDIPS.drag;
    // initialization
    rd.init();
    // only "smile" can be placed to the marked cell
    rd.mark.exception.d8 = 'smile';
    // prepare handlers
    rd.myhandler_clicked    = function () {document.getElementById('message').innerHTML = 'Clicked'}
    rd.myhandler_moved      = function () {document.getElementById('message').innerHTML = 'Moved'}
    rd.myhandler_notmoved   = function () {document.getElementById('message').innerHTML = 'Not moved'}
    rd.myhandler_dropped    = function () {document.getElementById('message').innerHTML = 'Dropped'}
    rd.myhandler_switched   = function () {document.getElementById('message').innerHTML = 'Switched'}
    rd.myhandler_clonedend1 = function () {document.getElementById('message').innerHTML = 'Cloned end1'}
    rd.myhandler_clonedend2 = function () {document.getElementById('message').innerHTML = 'Cloned end2'}
    rd.myhandler_notcloned  = function () {document.getElementById('message').innerHTML = 'Not cloned'}
    rd.myhandler_deleted    = function () {document.getElementById('message').innerHTML = 'Deleted'}
    rd.myhandler_undeleted  = function () {document.getElementById('message').innerHTML = 'Undeleted'}
    rd.myhandler_cloned     = function () {
        // display message
        document.getElementById('message').innerHTML = 'Cloned';
        // append 'd' to the element text (Clone -> Cloned)
        rd.obj.innerHTML += 'd';
    }
    rd.myhandler_changed    = function () {
        // define current row and current cell
        var ri = REDIPS.drag.current_cell.parentNode.rowIndex,
            ci = REDIPS.drag.current_cell.cellIndex;
        // display current row and current cell
        document.getElementById('message').innerHTML = 'Changed: ' + ri + ' ' + ci;
    }
}
// toggles trash_ask parameter defined at the top
function toggle_confirm(chk) {
    REDIPS.drag.trash_ask = chk.checked;
}
// toggles delete_cloned parameter defined at the top
function toggle_delete_cloned(chk) {
    REDIPS.drag.delete_cloned = chk.checked;
}
// enables / disables dragging
function toggle_dragging(chk) {
    REDIPS.drag.enable_drag(chk.checked);
}
// function sets drop_option parameter defined at the top
function set_drop_option(radio_button) {
    REDIPS.drag.drop_option = radio_button.value;
}
// show prepared content for saving
function save(){
    // scan first table
    var content = REDIPS.drag.save_content(1);

    // if content doesn't exist
    if (content === '') {
        alert('Table is empty!');
    }
    else {
        alert(content);
    }
    // display query string
    // else {
    //     //window.open('/my/multiple-parameters.php?' + content, 'Mypop', 'width=350,height=160,scrollbars=yes');
    //     window.open('multiple-parameters.php?' + content, 'Mypop', 'width=350,height=260,scrollbars=yes');
    // }
}
