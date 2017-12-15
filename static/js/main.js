var monthname=new Array("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec");

$(function(){
    $('.select2').select2();
    $('.select2-costcenter').select2({
        placeholder: function(){
            $(this).data('placeholder');
    }
});
});

function expand_collapse(flag) {
    if(flag==0)
    {
        $('.ts-expand').css('display', 'block')
        $('.ts-collapse').css('display', 'none')
        $('.ts-btn-collapse').css('display', 'none')
        $('.ts-btn-expand').css('display', 'inline-block')
    }
    else
    {
        $('.ts-btn-collapse').css('display', 'inline-block')
        $('.ts-btn-expand').css('display', 'none')
        $('.ts-expand').css('display', 'none')
        $('.ts-collapse').css('display', 'block')   
    }
}

$(window).bind("load", function() { 
     $('.label-select-box').closest('tr').find('button').hide();
     // if previous form date and current form date are the same
     //then hide day and date
     if ($("#formset_form").length){
        var all_forms = $('.dynamic-form');
        var previous_form = forms[0];
        for (var i=1; i<all_forms.length; ++i) {
            prev_val = $($(previous_form).children('td')[1]).find('input').val();
            current_val = $($(all_forms[i]).children('td')[1]).find('input').val();
            if (prev_val == current_val){
                var day_td = $(all_forms[i]).children('td')[0].children[0];
                var date_td = $(all_forms[i]).children('td')[1].children[0];
                $(day_td).hide();
                $(date_td).hide();
                deleteTriggerMarkup = '<a ' +
                                'class="delete_row" ' +
                                'href="javascript:void(0)">' + 'Remove' +
                                '</a>';
                $(all_forms[i]).children(':last').empty().append(deleteTriggerMarkup);
            }
            else
                previous_form = all_forms[i]
        }
        // hide the Add/Remove buttons when the tscodes are disabled.
        $(all_forms).each(function(){
            if ($($(this).children('td')[3].children[0]).find('select').is(':disabled'))
                $($(this).children(':last')).empty();
        })
     }
});

$(function(){
    expand_collapse(0);
    var startDate = new Date();
    var FromEndDate = new Date();
    var ToEndDate = new Date();
    FromEndDate.setDate(ToEndDate.getDate() + 30);
    ToEndDate.setDate(ToEndDate.getDate() + 30);

    $('#payroll_month').datepicker(
    {
         format: 'M/yyyy',
         minViewMode: "months"
    })
    $('.start_date').datepicker({
        format: 'dd/mm/yyyy',
        startDate: startDate,
        endDate: FromEndDate,
        autoclose: true
    })
    .on('changeDate', function (selected) {
        startDate = new Date(selected.date.valueOf());
        startDate.setDate(startDate.getDate(new Date(selected.date.valueOf())));
        $('.end_date').datepicker('setStartDate', startDate);
    });
    $('.end_date').datepicker({
        format: 'dd/mm/yyyy',
        startDate: startDate,
        endDate: ToEndDate,
        autoclose: true
    })
    .on('changeDate', function (selected) {
        FromEndDate = new Date(selected.date.valueOf());
        FromEndDate.setDate(FromEndDate.getDate(new Date(selected.date.valueOf())));
        $('.start_date').datepicker('setEndDate', FromEndDate);
    });


    $(".userswitchlist li a").click(function(){
        $("#username").val($(this).text());
        $("#userswitchform").submit();
    });

    $(".submit_weekly, .submit_leaverequest").click(function(){
        $("#submit_timesheet_form").submit();
    });

    var choose_all = ($("th[class='select_ts']").find("input"))[0];
    $(choose_all).on('change', function(event) {
      var checked = this.checked;
      var all_inputs = $("input[name='timesheets']");
      all_inputs.prop('checked', checked);
    });

    $(".choose_subordinates li a").click(function(event){
        event.preventDefault();
        var onbehalf_form = $("#submit_onbehalf");
        onbehalf_form.attr('action', this.href);
        onbehalf_form.submit();
    })

    Date.prototype.yyyymmdd = function() {
    var yyyy = this.getFullYear().toString();                                    
    var mm = (this.getMonth()+1).toString(); // getMonth() is zero-based         
    var dd  = this.getDate().toString();
    return (dd[1]?dd:"0"+dd[0]) + '/' + (mm[1]?mm:"0"+mm[0]) + '/' + yyyy ;
    };  

    $('.week-start-date').datepicker({
        // daysOfWeekDisabled: [1,2,3,4,5,6],
        // format: 'dd/mm/yyyy',
        format: 'yyyy-mm-dd',
        autoclose: true,
        todayHighlight:false,
    });

    $("#dashboard_date").datepicker({
        daysOfWeekDisabled: [1,2,3,4,5,6],
        format: 'dd/M/yyyy',
    })

    $("#select_year").on('click', function(e){
        var date_input = $("#dashboard_date");
        date_input.datepicker('remove');
        date_input.datepicker(
            {
                format: 'yyyy',
                minViewMode: "years"
            });
        $("#selection_dropdown").text('Yearly');
        date_input.val('');
        date_input.attr('placeholder', 'Select year');
    });

     $("#select_month").on('click', function(e){
        var date_input = $("#dashboard_date");
        date_input.datepicker('remove');
        date_input.datepicker(
            {
                format: 'M/yyyy',
                minViewMode: "months"
            });
        $("#selection_dropdown").text('Monthly');
        date_input.val('');
        date_input.attr('placeholder', 'Select month');
    });

      $("#select_week").on('click', function(e){
        var date_input = $("#dashboard_date");
        date_input.datepicker('remove');
        date_input.datepicker(
            {
                daysOfWeekDisabled: [1,2,3,4,5,6],
                format: 'dd/M/yyyy'
            });
        $("#selection_dropdown").text('Weekly');
        date_input.val('');
        date_input.attr('placeholder', 'Select date');
    });




// for the subordinate view GM and above
    $(".month_picker").datepicker( {
    format: "m/yyyy",
    viewMode: "months", 
    minViewMode: "months"
    });

    $("#this_week").on('click', function(e){
        var curr = new Date; // get current date
        var first = curr.getDate() - curr.getDay();
        var firstday = new Date(curr.setDate(first));
        $("#start_date").val(firstday.yyyymmdd())
    })
    $("#week_load").on('click', function(e){
        e.preventDefault();
        var start = $('#start_date').val();
        if (!start) {
            var url='/core/subordinates/';
        }
        else{
            start_arr = start.split('/');
            new_arr = start_arr.reverse();
            week_start = new_arr.join('/')
            var url='/core/subordinates/week/'+week_start+'/';
        }
        window.location.replace(url);
    })

      $("#this_month").on('click', function(e){
        var curr = new Date; // get current date
        var month = curr.getMonth()+1;
        var year = curr.getFullYear();
        $("#month").val(month+"/"+year);
        var monName = monthname[curr.getMonth()]; 
        $("#payroll_month").val(monName+"/"+year);
    })

    $("#month_load").on('click', function(e){

        e.preventDefault();
        var reversed = false;
        var bu_val = $("#unit").val();
        action_value  = $("#month_load").val()
        if(action_value=='payroll')
        {
            var base_url = '/core/payroll/'
            var month_val = $("#payroll_month").val();
            month_val = month_val.split('/').reverse().join('/');
            reversed = true;
        }
        else if(action_value=='sub_payroll')
        {
            subordinate_value = $("#payroll-subordinate").val()
            var base_url = '/core/payroll/'+subordinate_value+'/'
            var month_val = $("#payroll_month").val();
            month_val = month_val.split('/').reverse().join('/');
            reversed = true;
        }
        else if(action_value=='unit_load')
        {
            var base_url = '/core/units/hierarchical/';
            var month_val = $("#month").val();
            month_val = month_val.split('/').reverse().join('/');
            reversed = true;
        }
        else
        {
            var base_url = '/core/subordinates/'
            if (location.pathname.indexOf('gfc') != -1)
                base_url = '/core/subordinates/as/gfc/';
            if (location.pathname.indexOf('gm') != -1)
                base_url = '/core/subordinates/as/gm/';
            var month_val = $("#month").val();
        }
        if (month_val){
            if(action_value)
            {
                if (!reversed)
                    month_val = month_val.split('/').reverse().join('/');
                append_url = month_val;
                url = base_url+append_url.toLowerCase()+'/'
            }
            else
            {
                if (!reversed)
                    month_val = month_val.split('/').reverse().join('/');
                append_url = month_val;
                url = base_url+append_url+'/'
            }
        }
        if (bu_val){
            append_url = bu_val+'/'
            url = base_url+append_url;
        }
        if (month_val && bu_val){
            append_url = bu_val+'/'+month_val.split('-').reverse().join('/');
            url = base_url+append_url+'/';
        }
        if (location.search.split()[0] != "")
            window.location.replace(url+location.search.split()[0]);
        else
            if (action_value=='unit_load' && $("#subunits").is(':checked')){
                url = url+'?subunits=1'
                window.location.replace(url);
            }
            window.location.replace(url);
    })

});

$('#today').click(function(e)
{
    var latestSunday = new Date(new Date().setDate(new Date().getDate() - new Date().getDay()));
    $('#week_start_date').val(latestSunday.yyyymmdd())
})

$('#id_notes').blur(function(e)
{
  
  notes = $('#id_notes').val()
  $('[name="hidden_notes"').val(notes)

});

var form;
var transition;
$('.approval-btn').click(function(e)
{
    form =  $('.approval-btn').closest("form");
    transition = $(this).val()
    $("#notesmodal").modal('show');
    e.preventDefault()
});

$('.add-notes-form').click(function(e)
{   
    notes = $('#id_notes_form').val();
    value = $(this).val();
    $('<input />').attr('type', 'hidden')
          .attr('name', "transition")
          .attr('value', transition)
          .appendTo(form);
    $('#hidden_notes').val(notes);
    form.submit();
});

$('.add-notes').click(function(e)
{   
    notes = $('#id_notes').val()
    value = $(this).val()
    $('<input />').attr('type', 'hidden')
          .attr('name', "transition")
          .attr('value', transition)
          .appendTo(form);
    if(value == 'add-notes')
    {
      if(notes==null||notes==''&&typeof form=='undefined') //Error not shown while submission
      {
        $('.notes-alert').show();
        $("#id_notes").addClass('errorClass');
        $("#error").show()
        e.preventDefault()
      }    
      else
      {
        if(typeof form != 'undefined')
            {
             $('#hidden_notes').val(notes);
             form.submit();
            }
        if (typeof notes_textbox != 'undefined')
            notes_textbox.val(notes);
        $('#id_notes').val('')
        $("#notes-ss-modal").modal('hide');
        $("#id_notes").removeClass('errorClass');
        // TODO: Quickly hacked in
        $(notes_button_td).children()[0].className += ' btn-info';
        $("#error").hide()
        
      }
    }
    else
    {
      if (typeof form != 'undefined')
      {
        $("#notesmodal").modal('hide');
        $("#id_notes").removeClass('errorClass');
      }
      else
      {
        if (typeof notes_textbox != 'undefined')
            notes_textbox.val(notes);
        $(notes_button_td).find('span').remove()
        $('#id_notes').val('')
        $("#notes-ss-modal").modal('hide');
        $("#id_notes").removeClass('errorClass');
        $("#error").hide()
      }
    }
    has_star = $('body').find('span.notes-star')
    if(has_star.length > 0)
    {
        $('#note-notification-span').css('display', 'block')
    }
    else
    {
        $('#note-notification-span').css('display', 'none')   
    }
})

var notes_textbox;
var notes_button;
$('.open-notes-modal').click(function(e)
{ 
    $("#id_notes").removeClass('errorClass');
    $("#error").hide();
    append_notes = $(this).closest('tr').find('input[class="notes-field-hidden"]').val();
    $("#existing-notes").html(append_notes);
    notes_text_id = $(this).closest('tr').find('input[class="notes-modal-input"]').attr('id');
    notes_textbox = $('#'+notes_text_id)
    notes_button_td = $(this).closest('td')
    if(notes_textbox.val())
    {
        $('#id_notes').val(notes_textbox.val())
    }
    $("#notes-ss-modal").modal('show');
});


$('.ts-code-select').on('change', function() {
  closest_reg_hr = $(this).closest('tr').find('input[class="regular-hrs-box numberinput form-control"]').attr('id')
  if($(this).val() == 'm')
  {
    $('#'+closest_reg_hr).prop("readonly", false);
  }
  else if(!$(this).val())
  {
    $('#'+closest_reg_hr).prop("readonly", true);
    $('#'+closest_reg_hr).val('');
  }
  else
  {
    $('#'+closest_reg_hr).prop("readonly", true);
    $('#'+closest_reg_hr).val(TS_CODE_WORKING_HOURS[$(this).val()].toFixed(1));  
  }
  
});

$("#id_project").on('change', function() {
    project_id = $(this).val();
    url = '/core/project/assignment/'+project_id+'/';
    window.location.replace(url);
});

$("#submit-id-clear").click(function(e) {
    e.preventDefault();
    window.location.replace('/core/project/view/');
});

formClass = 'dynamic-form';
forms = $('.' + formClass);
childElementSelector = 'input,select,textarea,label,div',

$("#close-button").click(function() {
    $("#custom-alert").addClass("hidden");
});

customAlert = function(msg){
    $("#alert-text").text(msg);
    $("#custom-alert").removeClass("hidden");
}

updateElementIndex = function(elem, prefix, ndx) {
    var idRegex = new RegExp(prefix + '-(\\d+|__prefix__)-'),
        replacement = prefix + '-' + ndx + '-';
    if (elem.attr("for")) elem.attr("for", elem.attr("for").replace(idRegex, replacement));
    if (elem.attr('id')) elem.attr('id', elem.attr('id').replace(idRegex, replacement));
    if (elem.attr('name')) elem.attr('name', elem.attr('name').replace(idRegex, replacement));
    }

// Returns all the forms that are created for a partucular day
currentdayForms = function(current_day){
    var currentday_forms = [];
    $('.' + formClass).each(function(){
        date_val = $($(this).children('td')[1]).find('input').val();
        if (date_val == current_day)
            currentday_forms.push(this);
    })
    return currentday_forms
}

//get all the dates of the form in a list
getAllDates = function(){
    var dates_list = [];
    $(forms).each(function(){
       date_val = $($(this).children('td')[1]).find('input').val();
       if($.inArray(date_val, dates_list) === -1) dates_list.push(date_val); 
    })
    return dates_list;
}

// Returns the total regular hours and total overtime for a particular day
getTotalRegularTotalOvertime = function(current_day_forms){
    var total_overtime = 0;
    var total_regular_hours = 0;
    $(current_day_forms).each(function(){
        if ($(this).is(':visible')) {
            hours_val = parseInt($($(this).children('td')[4]).find('input').val());
            if (!hours_val)
                hours_val = 0;
            overtime_val = parseInt($($(this).children('td')[5]).find('input').val());
            total_regular_hours += hours_val;
            total_overtime += overtime_val;
        }
    })
    return [total_regular_hours, total_overtime];
};


$(".AddButton").click(function() {
    current_row = $(this).parent().parent();
    row = current_row.clone(true);
    $(row).children('input').val("");
    $($(row).children('td')[3]).find('select').val("");
    var day_td = $(row).children('td')[0].children[0];
    var date_td = $(row).children('td')[1].children[0];
    var regular_hrs_td = $(row).children('td')[4].children[0];
    var tscode_val = $($(current_row).children('td')[3]).find('select').val();
    if (!tscode_val){
        customAlert('Please select a status before adding new row');
        return false;
    }
    totalForms = $('#id_form-TOTAL_FORMS');
    var formCount = parseInt(totalForms.val());
    // Hide both the day and date elements
    $(day_td).hide();
    $(date_td).hide();
    $(regular_hrs_td).find('input').prop("readonly", true);
    $(regular_hrs_td).find('input').val('');
    $(row).insertAfter(current_row);
    row.find(childElementSelector).each(function() {
                    updateElementIndex($(this), 'form', formCount);
                });
    deleteTriggerMarkup = '<a ' +
                                'class="delete_row" ' +
                                'href="javascript:void(0)">' + 'Remove' +
                                '</a>';
    row.children(':last').empty().append(deleteTriggerMarkup)
    totalForms.val(formCount + 1);
});


$(document).on('click', '.delete_row', function()
{
    var row = $(this).parents('.' + formClass);
    $(row).find('.delete-row').val(true);
    row.hide();
});

// Some checks before form submission
submissionPreCheck = function(all_dates){
    var can_submit = true;
    $(all_dates).each(function(i, dt){
        date_forms = currentdayForms(dt);
        var regular_overtime = getTotalRegularTotalOvertime(date_forms);
        if (regular_overtime[0] > 8) {
            customAlert("Total regular hours for a day cannot be more than 8. Please review");
            can_submit = false;
        }
        if (regular_overtime[1] && regular_overtime[0] < 8){
            customAlert("You cannot add overtime hours unless cumulative regular hours is 8");
            can_submit = false;
        }
    });
    return can_submit;
}


$("#submit-weekly-form").click(function(e){
    e.preventDefault();
    var all_dates = getAllDates();
    var can_submit = submissionPreCheck(all_dates);
    if (can_submit)
        $("#formset_form").submit();
});

$('#frm_project_search').submit(function() {
    var value = $('#month').val().replace(' ','').split('/').map(parseFloat);
    var month = value[0],
        year = value[1];

    document.getElementById('input_month').value = month
    document.getElementById('input_year').value = year
    
    return true;
});

$('.file-style').filestyle({
    buttonName : 'btn-primary',
    buttonText : ' Browse'
});
