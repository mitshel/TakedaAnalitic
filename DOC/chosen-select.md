.chosen-container { width: 100% !important; }
.chosen-container-multi .chosen-choices li.search-choice {
    margin: 0px 0px 0px 3px;
    padding: 1px 20px 0px 3px;
    font-size: 10px;
}
.chosen-container-multi .chosen-choices li.search-choice .search-choice-close { top: 2px; }
.chosen-container-multi .chosen-choices li.search-field input[type="text"] { height: 14px; }
.chosen-container-multi .chosen-choices
{
  padding: 2px 5px;
  font-size: 12px;
  line-height: 1.5;
  border-radius: 1px;
}

                          {% if field.type == 5 %}
                             <div class="input-group input-group-xs">
                                <select data-placeholder="Выбор..." class="form-control chosen-select" multiple="" id="input_{{ field.name }}" tabindex="-1" style="display: none;">
                                </select>
                             </div>
                              <script>
                                    $("#input_{{ field.name }}").chosen();
                                    $('#input_{{ field.name }}_chosen .chosen-choices input').autocomplete({
                                      source: function( request, response ) {
                                        $.ajax({
                                          url: "{% url 'data:fk' field.fk %}"+request.term,
                                          dataType: "json",
                                          beforeSend: function(){$('#input_{{ field.name }}').empty();},
                                          success: function( data ) {
                                            response( $.map( data.items, function( item ) {
                                              $('#input_{{ field.name }}').append('<option value="'+item.id+'">' + item.name + '</option>');
                                            }));
                                            $("#input_{{ field.name }}").trigger("chosen:updated");
                                          }
                                        });
                                      }
                                    });
                              </script>
                          {% endif %}