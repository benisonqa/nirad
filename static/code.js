$(document).ready(function() {
	var xhr = null;
	$(".msg").parent().find('button').attr('disabled', true);
	$("#download").attr('disabled', true)
	$("#choose").click(function (){
		$(this).parent().find('button').click();
		
	});
	

	var ol = $('#upload ol');
    $('#browse a').click(function () {
        $(this).parent().find('input').click();
	});
	
	$('input[type="file"]').change(function(e){
		$(".upload-files-list").empty();
		var fileName = e.target.files[0].name;
		//alert('The file "' + fileName +  '" has been selected.');
		$(".upload-files-list").html(fileName);
		$(".upload-files-list").html(fileName);
			if ($(".upload-files-list").html(fileName) != ''){
				$(this).parent().find('button').show(); 
			}
		
	});
	
	$("form#data").submit(function(){
		$(".file-progress").show();
		$('.myprogress').css('width', '0');

    var formData = new FormData(this);
    $.ajax({
        url: "files-upload",
        type: 'POST',
        data: formData,
		//async: false,
		
		//this part is progress bar
		
		xhr: function (){
			var xhr = new window.XMLHttpRequest();
			xhr.upload.addEventListener("progress", function (evt) {
				if(evt.lengthComputable){
					var percentComplete = evt.loaded / evt.total;
					percentComplete = parseInt(percentComplete * 100);
					$('.myprogress').text(percentComplete + '%');
					$('.myprogress').css('width', percentComplete + '%');
				} //else { alert("Processing");};
			}, false);
			return xhr;
		},
				success: function (data) {
					//$(".msg").text(data);
					$("#choose b").css('color' , 'green');
					$(".msg").parent().find('button').attr('disabled', false);
					$("#uploading").parent().find('button').attr('disabled', true);
				},
				cache: false,
				contentType: false,
				processData: false
			});

			return false;
		});	
		
	$("#proceed").click(function(){
	    window.location.href= 'process';
	});
});