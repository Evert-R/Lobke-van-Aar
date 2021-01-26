// Set menu item active
$('#er-works-active').addClass('er-center-active');

// Remove the shop navigation
$('#er-shop-nav').addClass('d-none');

// Make filter submit on select
$('#id_cat').change(function () {
    $('#er-filter-works').submit();
});