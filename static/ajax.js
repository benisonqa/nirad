/*jslint browser: true*/
/*global $, jQuery, alert*/

$(document).ready(function() {
	$("#finish").prop('disabled' ,true);


var repeat = setInterval(complete, 200);

	function get_details(){
	$.ajax({
		url:"backend/details.txt",
		cache:false,
		success:function(data){
			$(".details").html(data);
		},
		//complete: function(){
			//setTimeout(get_details, 1500);
		//}
	});
}
	function complete(){
			$.ajax({
					url:"backend/progress.txt",
					cache: false,
					//async: false,
					success: function(value){
						if (value != '100.0%'){
							$(".progress-bar").html(parseFloat(value)+ '%');
							$(".progress-bar").css("width", value);
							get_details();
							}
						else{
							value = '100.0%';
							$(".progress-bar").html(value);
							$(".progress-bar").css("width", value);
							$("#download").attr('disabled', false)
							$("#finish").attr('disabled', false)
							clearInterval(repeat);
							}
								}
				});
			}

$.ajax({
	url: "backend/interface.php",
	cache:false,
	success:function(data){
		console.log('inside log')
		$("#output").show()
		$("#output").html(data);
	} 
})

$("#download").click(function(){
	window.location.href = 'backend/download.php';	
	});

$("#finish").click(function(){
	window.location.href = 'index.html';	
	});


});