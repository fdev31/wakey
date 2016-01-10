var NAME = null
var button_list = []

function strip(text) {
    return text.match('^ *(.*?) *$')[1]
}
function refresh_options() {
    var have_args = $('#option_type').val() !== 'modetoggle'
    if (have_args) {
        $('#value_popup_options').show()
    } else {
        $('#value_popup_options').hide()
    }

}
function import_defaults() {
    snap.selectAll('text[wakey] > tspan').forEach( function(e) {
        e.node.innerHTML = 'button'
    } )
}
function import_config() {
    // set globals
    CONF = JSON.parse($('#device_description').val())
    for (var k in CONF) { break }
    if (NAME !== k ) {
        NAME = k
        Snap.load("models/"+NAME+"/template.svg", function(canvas) {
            on_main_canvas_loaded(canvas)
            apply_config()
        });
    } else {
        apply_config()
    }
    window.scrollTo(0, 0)
    $('#more_info').addClass('transparent')
    setTimeout( function() { $('#more_info').css('display', 'none') }, 1200)
    return false
}
function export_config() {
    var text = []
    for (var button in button_list) {
        button = button_list[button]
        text.push(strip('xsetwacom set "'+button.dev+'" Button '+button.name.split(':')[1]+' "'+get_button_text(button.name).node.innerHTML+'"'))
    }
    $('#sourcecode').html(text.join(';<br/>') + '\n<br/>\n<br/>\n<br/>\n')
}
function get_button_text(item) {
    return snap.select('text[wakey="'+item+'"] tspan')
}
function apply_value() {
    var text = get_button_text( $('#value_popup').data('wakey') )
    text.node.innerHTML = strip($('#option_type').val() + ' ' + $('#option_argument').val())
    $('#value_popup').css('visibility', 'hidden')
}
function _change_value_cb(ev) {
    var old_value = ev.target.innerHTML
    if (!!old_value.match(/^m/)) { // menutoggle
        $("#option_type").val("modetoggle")
    } else {
        $("#option_argument").val(strip(old_value.substr(1 + old_value.split(' ', 1)[0].length)))
        if(old_value.match(/^b/)) {
            $("#option_type").val("button")
        } else {
            $("#option_type").val("key")
        }
    }
    if (ev.clientY > $(window).height() / 2) {
        var y = ev.clientY - $('#value_popup').height();
    } else {
        var y = ev.clientY;
    }
    if (ev.clientX > $(window).width() / 2) {
        var x = ev.clientX - $('#value_popup').width();
    } else {
        var x = ev.clientX;
    }
    $('#value_popup').css({'margin-left': x, 'margin-top': y })
    $('#value_popup').css('visibility', 'visible')
    $('#value_popup').data('wakey', ev.target.parentNode.getAttribute('wakey'))
    $('#option_argument').focus()
}
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
    snap.children().forEach( function(o) { o.remove() } )
    snap.add(main_canvas)
}
