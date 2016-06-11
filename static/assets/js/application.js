$(function () {
    // Initialize the sidebar state based
    // on the current screen size
    toggleSidebar();

    $(window).resize(function () {
        toggleSidebar()
    });
    
    function toggleSidebar() {
        if($(window ).width() >= 1180){
            $('#sidebar-toggle').toggle(false);
            $('#sidebar').toggle(true)
        }else {
            $('#sidebar-toggle').toggle(true);
            $('#sidebar').toggle(false)
        }
    }
    
    $("#sidebar-toggle").on("click", function () {
        $('#sidebar').toggle()
    })
});