
function testalert(){
	alert('test');
}



function ShowMessage(data)
	{

	
	if(data.success)
					{
					$('#success').show();
					$('#error').hide();
					$(".success-msg").text("");
					$(".success-msg").append(' <i class="fa fa-check"></i>  ');
					$(".success-msg").append(data.success);
					if (data.redirect)
								{
								
								window.location.href = data.redirect;

								}
					}
	else if (data.error)
					{

					$('#error').show();
					$('#success').hide();
					$(".error-msg").text("");
					$(".error-msg").append(' <i class="fa fa-times-circle"></i> ');
					$(".error-msg").append(data.error);
					}
	}


/*materialize css js script required for components*/
$(".button-collapse").sideNav();

$('.datepicker').pickadate({
format: 'yyyy-mm-dd',
selectMonths: true, // Creates a dropdown to control month
selectYears: 100, // Creates a dropdown of 15 years to control year,
today: 'Today',
clear: 'Clear',
close: 'Ok',
closeOnSelect: false // Close upon selecting a date,
});	


$('.dropdown-button').dropdown({

inDuration: 300,
outDuration: 225,
constrainWidth: false, // Does not change width of dropdown to that of the activator
hover: true, // Activate on hover
gutter: 0, // Spacing from edge
belowOrigin: true, // Displays dropdown below the button
alignment: 'left', // Displays dropdown with edge aligned to the left of button
stopPropagation: false // Stops event propagation

}
);

$('select').material_select();

/*materialize css js script required for components*/
