//if click on create:
document.getElementById('create').addEventListener('click', function(){
	document.querySelector('.create-group').style.display = 'flex';
});

//if click on join:
document.getElementById('join').addEventListener('click', function(){
	document.querySelector('.user-set-up').style.display = 'flex';
});

/*
 * index 0 : from group to code
 * index 1 : from codes to maker
*/
var modalTransitions = [
	function(){
		document.querySelector('.create-group').style.display = 'none';
		document.querySelector('.create-codes').style.display = 'flex';
	}, 
	function(){
		document.querySelector('.create-codes').style.display = 'none';
		document.querySelector('.maker-set-up').style.display = 'flex';
	},
	function(){
		console.log("CHECK");
	}
];

//state regulation
var add_codes_clicked = false;
document.getElementById('add_codes').addEventListener('click', function(){
	add_codes_clicked = true;
});
 //code list regulation:
var previousCode = null;

var ajaxCall = function(formName, path, transition_index){
	$(formName).on('submit', function(e){
		e.preventDefault();
		var group = $(this),
			url = path,
			type = group.attr('method'),
			data = {};
		group.find('[name]').each(function(index, value){
			var name = $(this).attr('name'),
				value = $(this).val();

			data[name] = value;
		});
		
		$.ajax({
			url: url,
			type: type,
			data: data,
			success: function(response){
				$(formName).trigger("reset");

			 	if (response.includes("Error")){
					alert(response);
				}

				else if(add_codes_clicked){
					var codeListArr = JSON.parse(response)
					//to display data in html dynamically: sometimes the list is made backwards
					if (previousCode != codeListArr[codeListArr.length - 1].fields.name){
						$(".code-list").prepend("<p>" + codeListArr[codeListArr.length - 1].fields.name + "</p>")
						previousCode = codeListArr[codeListArr.length - 1].fields.name;
					}
					else{
						$(".code-list").prepend("<p>" + codeListArr[0].fields.name + "</p>")
					}
					//state regulation
					add_codes_clicked = false;
				}

				else{
					modalTransitions[transition_index]();
					//assuming we're at the endpoint of out first page and there are no errors/alerts:
					if(transition_index == 2){
						location.href = "bulletin";
					}
				}
			}
		}); 
	});
}

//making group page functionality:
ajaxCall('form.group', 'process-group', 0);
ajaxCall('form.codes', 'process-codes', 1);
ajaxCall('form.maker', 'process-maker', 2);
ajaxCall('form.user', 'process-user', 2);