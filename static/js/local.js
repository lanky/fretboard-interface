// vim: set ts=2 sts=2 sw=2 ci nu ft=javascript:
$(document).ready(function(){
  $('#addmarker').click(function(e){
    event.preventDefault();
    var nextindex = $('.extras_row').length;
    $('#extras').append(`<tr data-toggle="fieldset-entry" class="extras_row">
      <td><input class="form-control form-control-sm col-sm-1 tooem" id="extras-${nextindex}-string" name="extras-${nextindex}-string" type="text"></td>
      <td><input class="form-control form-control-sm col-sm-1 tooem" id="extras-${nextindex}-fret" name="extras-${nextindex}-fret" type="text"></td>
      <td><input class="form-control form-control-sm col-sm-1 tooem" id="extras-${nextindex}-marker" name="extras-${nextindex}-marker" type="text"></td>
      <td><input type="button" class="delmarker" value="-" id="extras-${nextindex}-delmarker" title="remove the current row"></input></td>
      </tr>`);
  });

  $('#extras').on('click', '.delmarker', function(e) {
    event.preventDefault();
    $(this).closest('tr').remove();
  });

});
