
$(function () {
    $('img').click(function () {
    console.log('点到我了');

    // $(this).src = 'app/getcode/';
    $(this).attr('src','/app/getcode/?t='+ Math.random());


    })

})
//
// $(function () {
//     $('.f5').click(function () {
//     console.log('点到我了');
//     $(this).attr('src','/app/getcode/?t='+ Math.random());
//
//
//     })
//
// })