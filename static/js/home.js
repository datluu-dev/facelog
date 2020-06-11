// var img_lens = [...Array(120).keys()];

$(document).ready(function(){
	host_location = window.location.host
	// source_url = host_location + "/get_img";
	$.get("/get_img", function(data){
		$('#pagination-region-1, #pagination-region-2').pagination({
			dataSource: data,
			pageSize: 12,
			locator: 'data',
			showPageNumbers: false,
			showNavigator: true,
			callback: function(data, pagination) {
				var html_code =  ""
				$.each(data, function(index, item){
					console.log(item)
					image_html_region = `
					   <div class="col-lg-3 col-md-4 col-6">
					      <a href="#" class="d-block mb-4 h-100">
					            <img class="img-fluid img-thumbnail" src="/${item["img_path_result"]}" alt="">
					          </a>
					    </div>
					`
					html_code += image_html_region
				})
				$('#img-region').html(html_code)
			}
		})
	})
})
