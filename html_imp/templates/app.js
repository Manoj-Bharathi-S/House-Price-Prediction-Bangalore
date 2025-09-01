function getBathValue() {
  var uiBathrooms = document.getElementsByName("uiBathrooms");
  for(var i in uiBathrooms) {
    if(uiBathrooms[i].checked) {
        return parseInt(i)+1;
    }
  }
  return -1; // Invalid Value
}

function getBHKValue() {
  var uiBHK = document.getElementsByName("uiBHK");
  for(var i in uiBHK) {
    if(uiBHK[i].checked) {
        return parseInt(i)+1;
    }
  }
  return -1; // Invalid Value
}

function onClickedEstimatePrice() {
  console.log("Estimate price button clicked");
  var sqft = document.getElementById("uiSqft");
  var bhk = getBHKValue();
  var bathrooms = getBathValue();
  var location = document.getElementById("uiLocations");
  var estPrice = document.getElementById("uiEstimatedPrice");

  var url = "/predict_home_price"; // Using relative URL since we're serving from the same domain

  const requestData = {
      total_sqft: parseFloat(sqft.value),
      bhk: bhk,
      bath: bathrooms,
      location: location.value
  };
  
  console.log('Sending request to:', url);
  console.log('Request data:', requestData);
  
  $.ajax({
      url: url,
      type: 'POST',
      contentType: 'application/json',
      data: JSON.stringify(requestData),
      success: function(data, status, xhr) {
          console.log('Response status:', status);
          console.log('Response data:', data);
          if (data.estimated_price !== undefined) {
              estPrice.innerHTML = "<h2>" + data.estimated_price.toString() + " Lakh</h2>";
          } else if (data.error) {
              console.error('Server error:', data.error);
              estPrice.innerHTML = "<h2 style='color:red'>Error: " + data.error + "</h2>";
          } else {
              console.error('Unexpected response format:', data);
              estPrice.innerHTML = "<h2 style='color:red'>Unexpected response from server</h2>";
          }
      },
      error: function(xhr, status, error) {
          console.error('Request failed:', status, error);
          console.error('Response text:', xhr.responseText);
          estPrice.innerHTML = "<h2 style='color:red'>Error: " + status + "</h2>";
      }
  });
}

function onPageLoad() {
  console.log( "document loaded" );
  var url = "/get_location_names"; // Using relative URL since we're serving from the same domain
  $.get(url,function(data, status) {
      console.log("got response for get_location_names request");
      if(data) {
          var locations = data.locations;
          var uiLocations = document.getElementById("uiLocations");
          $('#uiLocations').empty();
          for(var i in locations) {
              var opt = new Option(locations[i]);
              $('#uiLocations').append(opt);
          }
      }
  });
}

window.onload = onPageLoad;
