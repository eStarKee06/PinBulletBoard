
//init bulletin page:
$( window ).on( "load", function() { 
	$.ajax({
		url: 'initialize-user',
		success: function(response){
			if (response == "false"){ // not the maker
				$("#delete-codes-btn").hide();
				$("#delete-group-btn").hide();
				$("#delete-codes-btn").attr("disabled", true);
				$("#delete-group-btn").attr("disabled", true);
				$("#delete-code-pmt").attr("disabled", true);
				$("#done-delete-code").attr("disabled", true);
				$("#delete-group-yes").attr("disabled", true);
				$("#cancel-delete-group").attr("disabled", true);
			}
			else{
				$("#delete-codes-btn").show();
				$("#delete-group-btn").show();
				$("#delete-codes-btn").attr("disabled", false);
				$("#delete-group-btn").attr("disabled", false);
				$("#delete-code-pmt").attr("disabled", false);
				$("#done-delete-code").attr("disabled", false);
				$("#delete-group-yes").attr("disabled", false);
				$("#cancel-delete-group").attr("disabled", false);
			}
		}
	}); 
})

//---------------------------------------------------------------------------------delete codes page------------------------------------------------------------
//go to delete codes page
document.getElementById("delete-codes-btn").addEventListener('click', function(e){
	document.querySelector('.delete-codes-ext').style.display = 'flex';
	e.preventDefault();
	$(".code-list-select").empty();
	$.ajax({
		url: 'list-codes',
		type: $(this).attr('method'),
		success: function(response){
			var codeListArr = JSON.parse(response);
			
			//$(".code-list-select").attr("size", codeListArr.length); 
			for(var i = 0; i < codeListArr.length; i++){
				console.log(codeListArr.length);
				if(codeListArr[i].fields.maker != true){
					$(".code-list-select").prepend("<option value=" + codeListArr[i].fields.name + ">" + codeListArr[i].fields.name + "</option>");
				}
			}
		}
	}); 
});

//if codes are deleted
document.getElementById("delete-code-pmt").addEventListener('click', function(e){
	var codesToBeDeleted;
	$('.code-list-select').each(function() {
		codesToBeDeleted = $('.code-list-select').val()
	});

	document.querySelector('.delete-codes-ext').style.display = 'none';
	e.preventDefault();

	$.ajax({
		url: 'delete-codes',
		type: 'POST',
		data: {'data': codesToBeDeleted },
		success: function(response){
		}
	}); 
});

// from delete codes to bulletin
document.getElementById("done-delete-code").addEventListener('click', function(){
	document.querySelector('.delete-codes-ext').style.display = 'none';
});


//------------------------------------------------------------------------------------------------delete Group Page----------------------
//go to group page
document.getElementById("delete-group-btn").addEventListener('click', function(e){
	document.querySelector('.delete-group-ext').style.display = 'flex';	
});

//from group page to bulletin
document.getElementById("cancel-delete-group").addEventListener('click', function(){
	document.querySelector('.delete-group-ext').style.display = 'none';
});

//delete group
document.getElementById("delete-group-yes").addEventListener('click', function(e){
	e.preventDefault();
	$.ajax({
		url: 'delete-group',
		type: $(this).attr('method'),
		success: function(response){
			window.location.href = "http://localhost:8000"; //note to self: must change that when published
		}
	}); 
});

//-------------------------------------------------------------------posts------------------------------------------------------------------------------------
document.getElementById("add-post-btn").addEventListener('click', function(e){
	document.querySelector('.make-posts-ext').style.display = 'flex';	
});

//state regulation
var addFileClicked = false; 

document.getElementById("make-post").addEventListener('click', function(e){
	if(addFileClicked){ //if media was added
		e.preventDefault();	
		data = new FormData($(".media-add-form" ).get(0));
		console.log($(".media-add-form" ).get(0));
		$.ajax({
			url: 'add-file',
			type: 'POST',
			data: data,
			processData: false,
			contentType: false,
			success: function(response){
				location.reload(true);
			}
		}); 
		addFileClicked = false; 
	}

	else{ //if no media
		e.preventDefault();	
		data = {};
		$(".make-post-form").find('[name]').each(function(index, value){
			var name = $(this).attr('name'),
				value = $(this).val();
				data[name] = value; 
		});

		$.ajax({
			url: 'make-post',
			type: $(".make-post-form").attr('method'),
			data: data,
			success: function(response){
				if (response.includes("Error")){ //code no longer existent
					alert(response);
					window.location.href = "http://localhost:8000";
				}
				else if (response != ""){ //no title problem
					alert(response);
				}
				else{
					location.reload(true); //reload bulletin to update the view
				}
			}
		});
	}

	$(".make-post-form").trigger("reset");
	$(".media-add-form").trigger("reset");
	document.querySelector('.media-add-form').style.display = 'none';
	document.querySelector('.make-posts-ext').style.display = 'none';
});

document.getElementById("add-file").addEventListener('click', function(e){
	addFileClicked = true; 

	e.preventDefault();	
	data = {};
	$(".make-post-form").find('[name]').each(function(index, value){
		var name = $(this).attr('name'),
			value = $(this).val();
			data[name] = value; 
	});

	$.ajax({
		url: 'make-post',
		type: $(".make-post-form").attr('method'),
		data: data,
		success: function(response){
			if (response.includes("Error")){
					alert(response);
					window.location.href = "http://localhost:8000";
			}
			else if (response != ""){
				alert(response);
				location.reload(true);
			}
		}
	}); 
	document.querySelector('.media-add-form').style.display = 'flex';
});

//-----------------------------------------------------------------------------------------------------------------
//user log out
document.getElementById("log-out").addEventListener('click', function(e){
		e.preventDefault();	
	$.ajax({
		url: 'log-out',
		success: function(response){
			window.location.href = "http://localhost:8000";
		}
	}); 
});