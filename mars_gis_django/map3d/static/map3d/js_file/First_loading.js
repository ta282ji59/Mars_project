/**
 * 始めの火星マップが完成するまでの無様な姿を隠すために書いた。
 * 使用してない
 */

$(function(){
    //umemo 5秒待つ
    setTimeout('stopload1()',5000);
});
function stopload1(){
    $('.body').delay(600).fadeOut(300);
    $('.header').delay(600).fadeOut(300);
    $('.grad').delay(600).fadeOut(300);
    $('#load').delay(600).fadeOut(300);
    $(function(){
        //umemo 0.6秒待つ
        setTimeout('stopload2()',600);
    });
}
function stopload2(){
    $('.body').css('z-index',0);
    $('.header').css('z-index',0);
    $('.grad').css('z-index',0);
    $('#load').css('z-index',0);
}