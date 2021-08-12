$(document).ready(function(){

    // Modal also used on Savour project and taken and adapted to this project
    // Update the modal content with information that has to be deleted
    // Credit code https://getbootstrap.com/docs/4.6/components/modal/
    $('#deleteModal').on('show.bs.modal', function (event) {
        // Button that triggered the modal
        let button = $(event.relatedTarget);

        // Extract info from data-* attributes
        let item = button.data('item');
        let item_url = button.data('url');

        // Update the modal's content
        let modal = $(this);
        modal.find('.delete-modal-title-item').text(item);
        modal.find('#btn-modal-confirm-delete').attr('href', item_url);
    });

    // Clear the fields from the modal when the modal is hidden / close
    $('#deleteModal').on('hidden.bs.modal', function () {
        let modal = $(this);
        modal.find('.delete-modal-title-item').text('');
        modal.find('#btn-modal-confirm-delete').attr('href', '');
    });
    // End Credit code

});