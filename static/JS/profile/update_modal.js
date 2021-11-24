/**
//  return the input field
// ajax request send
 * @param {*} field 
 */
function get_modal(field) {
    var urlKeyword = field_url(field);
    var mainContainer = document.getElementById('#base-container');
    var modalElement = document.getElementById(`${urlKeyword}-modal`);
    if (modalElement == null) {
        $.ajax({
            url: `/update/${urlKeyword}/`,
            type: 'GET',
            data: {
                'urlKeyword': urlKeyword,
                'field': field
            }
        }).done(function (response) {
            // console.log(response);
            if (response.data) {
                var modalBody = `
                        ${csrf_token}
                        <div class="form-group">
                            <input type="text" class="form-control" id="old-${urlKeyword}" value='${response.data}'>
                        </div>
                        ${response.input}`;
                var modalHTML = createModal(field, urlKeyword, modalBody);
                $(modalHtml).insertAfter(mainContainer);

                $(`#${urlKeyword}-modal`).show();


            }
            else {
                var modalBody = `
                        ${csrf_token}
                        <div class="form-group">
                            <input type="text" class="form-control" id="old-${urlKeyword}" value='Invalid Data!'>
                        </div>
                        <div class="form-group">
                            <input type="text" class="form-control" id="new-${urlKeyword}" placeholder="Invalid Field" name="data">
                        </div>`;
                var modalHTML = createModal(field, urlKeyword, modalBody);
                $(modalHtml).insertAfter(mainContainer);
            }
        })
            .fail(function () {
                console.log("failed");
            })


    }
    $(`#${urlKeyword}-modal`).show();


}


/**
 * function close the update modal
 * @param {*} id 
 */
function closeUpdateModal(id) {
    var modalElement = document.getElementById(id);
    modalElement.style.display = 'none';
}


/**
 * take the field name and return the appropriate url keyword
 * @param {*} field 
 * @returns urlKeyword
 */
function field_url(field) {
    field = field.toLowerCase();
    field = field.replace(' ', '_');
    field = field.replace('.', '');
    return field;
}


/**
 * Return the modal HTML
 * @param {*} field 
 * @param {*} urlKeyword 
 * @param {*} modalBody
 */
function createModal(field, urlKeyword, modalBody) {
    var valueElement = document.getElementById(`value-${urlKeyword}`);
    var value = valueElement.innerText;

    // html code for modal
    modalHtml = `
        <div class="modal" id='${urlKeyword}-modal' tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header border-top-0">
                        <h5 class="modal-title font-weight-bold">Update ${field}</h5>
                        <button type="button" class="close" data-dismiss="modal" aria-label="Close" onclick="closeUpdateModal('${urlKeyword}-modal')">
                            <span aria-hidden="true">&times;</span>
                        </button>
                    </div>
                    <form method="POST" action="/update/${urlKeyword}/" id='${urlKeyword}-modal-form'>
                    <div class="modal-body">
                        ${modalBody}    
                    </div>
                        <div class="modal-footer border-bottom-0">
                            <button type="submit" class="btn btn-primary my-btn"> Update</button>
                            <button type="button" class="btn btn-secondary my-btn" data-dismiss="modal" onclick="closeUpdateModal('${urlKeyword}-modal')">Close</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>`;

    return modalHtml;
}
