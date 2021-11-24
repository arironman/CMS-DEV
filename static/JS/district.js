// Dynamic district and pincode

/**
 * requesting and adding districts according to the state
 */
function addDistrict(element, addressType) {
    var state = (element.value || element.options[element.selectedIndex].value);
    
    if (state != "" || state != 'State') {
        $.ajax({
            url: '/district/',
            type: 'GET',
            data: { state: state }
        }).done(function (response) {
            if (response.status) {
                var districtElement = document.getElementById(`${addressType}-district`);
                districtElement.innerHTML = '';
                var districtHTML = '';
                for (let index = 0; index < response.district.length; index++) {
                    districtHTML += `<option value="${response.district[index]}">${response.district[index]}</option>`;
                }

                districtElement.innerHTML += districtHTML;
            }
            else {
                var districtElement = document.getElementById(`${addressType}-district`);
                districtElement.innerHTML += '<option value="">No District Found</option>';
            }
        })
            .fail(function () {
                console.log("failed");
            })
    }
}




/**
 * requesting and adding Pincodes according to the district
 */
function addPincode(element, addressType) {
    var district = (element.value || element.options[element.selectedIndex].value);

    if (district != "" || state != 'district') {
        $.ajax({
            url: '/pincode/',
            type: 'GET',
            data: { district: district }
        }).done(function (response) {
            if (response.status) {
                var pincodeElement = document.getElementById(`${addressType}-pincode`);
                pincodeElement.innerHTML = '';
                var pincodeHTML = '';
                for (let index = 0; index < response.pincodes.length; index++) {
                    pincodeHTML += `<option value="${response.pincodes[index]}">${response.pincodes[index]}</option>`;
                }

                pincodeElement.innerHTML += pincodeHTML;
            }
            else {
                var pincodeElement = document.getElementById(`${addressType}-pincode`);
                pincodeElement.innerHTML += '<option value="">No Pincode Found</option>';
            }
        })
            .fail(function () {
                console.log("failed");
            })
    }
}






/**
 * requesting and adding Pincode according to the districts
 */
// function addPincode(element, addressType) {
//     var district = (element.value || element.options[element.selectedIndex].value);
//     if (district != "" || district != 'District') {
//         $.ajax({
//             url: `https://api.postalpincode.in/postoffice/${district}`,
//             type: 'GET',
//             data: {}
//         }).done(function (response) {
//             if (response[0].Status == 'Success') {
//                 var pincodeElement = document.getElementById(`${addressType}-pincode`);
//                 pincodeElement.innerHTML = '';
//                 var pincodeHTML = '';
//                 for (let index = 0; index < response[0].PostOffice.length; index++) {
//                     pincodeHTML += `<option value="${response[0].PostOffice[index].Pincode}">${response[0].PostOffice[index].Pincode}</option>`;
//                 }

//                 pincodeElement.innerHTML += pincodeHTML;
//             }
//             else {
//                 var pincodeElement = document.getElementById(`${addressType}-pincode`);
//                 pincodeElement.innerHTML += '<option value="">No Pincode Found</option>';
//             }
//         })
//             .fail(function () {
//                 console.log("failed");
//             })
//     }
// }


