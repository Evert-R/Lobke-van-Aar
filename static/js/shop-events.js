// Set shop menu item active

$('#er-shop-active').addClass('er-center-active');
$('.er-shop-info').fadeOut(20000);

// Make filter submit on select
$('#id_type').change(function () {
    $('#er-shop-filter').submit();
});
$('#id_size').change(function () {
    $('#er-shop-filter').submit();
});
$('#id_mat').change(function () {
    $('#er-shop-filter').submit();
});