/**
 * Created by Yooke on 2017/3/29.
 */
$ (function () {
    $('.navbar-inverse').mouseenter(function () {
        $(this).css("opacity",'0.9')
    });
    $('.navbar-inverse').mouseleave(function () {
        $(this).css("opacity",'0.2')
    })
  })



function showToolTip(name, time, abstract) {
    $('#tooltip a').html('<h3>'+name+'</h3>');
    $('#tooltip p:first').text('19' + time);
    $('#tooltip p:eq(1)').text(abstract);
    $('#tooltip').css({'display': 'block', 'position': 'absolute', 'zIndex': '1'})
}
