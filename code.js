var NAME = 'Wacom Intuos PT S'

function import_config() {
    CONF = JSON.parse($('#device_description').val())
    apply_config()
    window.scrollTo(0, 0)
    return false
}

function export_config() {
    var text = []
    for (var button in button_list) {
        button = button_list[button]
        text.push('xsetwacom set "'+button.dev+'" Button '+button.name.split(':')[1]+' "'+get_button_text(button.name).node.innerHTML+'"')
    }
    $('#sourcecode').html(text.join(';<br/>') + '\n<br/>\n<br/>\n<br/>\n')
}

function get_button_text(item) {
    return snap.select('text[wakey="'+item+'"] tspan')
}

function _change_value_cb(ev) {
    $('.helpgroup').css('visibility', 'visible')
    var old_value = ev.target.innerHTML
    val = window.prompt("Enter new value", old_value) || old_value
    ev.target.innerHTML = val
    $('.helpgroup').css('visibility', 'hidden')
}

var button_list = []
function install_handlers(device, item, text) {
    var match = get_button_text(item)
    if (!!match) {
        match.node.innerHTML = text
        match.node.onclick = _change_value_cb
        button_list.push( {'dev': device, 'name': item} )
    }
}

function apply_config() {
    button_list = []
	var tablet = CONF[NAME]
    for (var dev_id in tablet) {
        for (var prop_id in tablet[dev_id]) {
            install_handlers(dev_id, prop_id, tablet[dev_id][prop_id])
        }
    }
}
function on_main_canvas_loaded(main_canvas) {
    snap = Snap('#diagram')
    snap.add(main_canvas)
    snap.selectAll('text[wakey] > tspan').forEach( function(e) {e.node.innerHTML='N/A'} )
}

$(function() {
    Snap.load("models/"+NAME+"/template.svg", on_main_canvas_loaded);
})

function show_app() {
	$('#input_zone').css('display', 'block')
	$('#diagram').css('display', 'block')
}
