$(document).ready(function(){

    /**
     * Call the toast method
     */
    $('.toast').toast('show');

    /**
     * Back to Top Button
     */
    $('.btt-link').click(function(e) {
        window.scrollTo(0,0);
    });

    /**
     * Toggle Back to Top button when the user scrolls down 20px from the top
     */
    window.onscroll = function() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            $('.btt-button').css('display', 'block');
        } else {
            $('.btt-button').css('display', 'none');
        }
    };
    
    /**
     * Make the collapse navbar menu scroll on mobile, tablets, if needed, and disable the scroll on body
     */
    $("button.navbar-toggler").on("click touchstart", function(){
        if ($("button.navbar-toggler").attr("aria-expanded") == "false") {
            $(".navbar").addClass("enable-scroll-mobile-menu");
            $("html body").addClass("disable-scroll-on-body");

        }
        else {
            $(".navbar").removeClass("enable-scroll-mobile-menu");
            $("html body").removeClass("disable-scroll-on-body");
        }
    });

    /**
     * Toggle the navbar menu, if open, with search form
     */
    $("a#mobile-search").on("click touchstart", function(){
        if ($("a#mobile-search").attr("aria-expanded") == "false" && ($("button.navbar-toggler").attr("aria-expanded") == "true")) {
            $("button.navbar-toggler").click();
        }
    });

    /**
     * Toggle the navbar menu, if open, with user-options
     */
    $("a#user-options-mobile").on("click touchstart", function(){
        if ($("a#user-options-mobile").attr("aria-expanded") == "false" && ($("button.navbar-toggler").attr("aria-expanded") == "true")) {
            $("button.navbar-toggler").click();
        }
    });

    /**
     * Close the collapse navbar menu when click outside the navbar
     *  @param {Object} event - Click event from element that was click
     */
    $(document).on("click touchstart", function(event){
        if ($("button.navbar-toggler").attr("aria-expanded") == "true" && $(event.target).closest(".navbar").length == 0) {
            $("button.navbar-toggler").click();
        }
    });

    
    /**
     * Update the modal content with information that has to be deleted
     * @param {Object} event - Click event from button that was click
     */
    $('#deleteModal').on('show.bs.modal', function (event) {
        // Button that triggered the modal
        var button = $(event.relatedTarget);

        // Extract info from data-* attributes
        var item = button.data('item');
        var item_url = button.data('url');

        // Update the modal's content
        var modal = $(this);
        modal.find('.delete-modal-title-item').text(item);
        modal.find('#btn-modal-confirm-delete').attr('href', item_url);
    });

    /**
     * Clear the fields from the modal when the modal is hidden / close
     */
    $('#deleteModal').on('hidden.bs.modal', function () {
        var modal = $(this);
        modal.find('.delete-modal-title-item').text('');
        modal.find('#btn-modal-confirm-delete').attr('href', '');
    });

});