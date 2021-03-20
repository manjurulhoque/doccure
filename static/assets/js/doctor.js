$(document).ready(function () {

    $('.day_option').on('change', function () {
        let val = $(this).val();

        if ($(this).prop('checked')) {
            $('.hideable_' + val).slideDown();
        } else {
            $('.hideable_' + val).slideUp();
        }
        return false;
    });

    $(".add_time_row").on('click', function (e) {
        e.preventDefault();

        let val = $(this).attr("data-id");
        $('.houritem_' + val).append(`
                <div class="row new_item_row_` + val + `">
                    <div class="col-sm-5 pr-0 mb-2">
                        <div class="input-group">
                            <div class="input-group-prepend">
                              <span class="input-group-text"><i class="fa fa-clock"></i></span>
                            </div>
                            <input type="text" class="form-control timepicker" name="start_time_` + val + `" value="" autocomplete="off">
                        </div>
                    </div>

                    <div class="col-sm-5 mb-2">
                        <div class="input-group">
                            <div class="input-group-prepend">
                              <span class="input-group-text"><i class="fa fa-clock"></i></span>
                            </div>
                            <input type="text" class="form-control timepicker" name="end_time_` + val + `" value="" autocomplete="off">
                        </div>
                    </div>

                    <div class="col-sm-2 mb-2 mt-2">
                        <a href="javascript:void(0);" class="remove_time_row text-danger"><i class="fa fa-trash"></i></a>
                    </div>
                </div>
            `);
    });

    $(".main_item").on('click', '.remove_time_row', function () {
        $(this).parent().parent().remove();
    });
});