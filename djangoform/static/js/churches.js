
document.addEventListener("DOMContentLoaded", function () {

  //helper func
  getElem = function (elemID) {
    const returnObj = document.getElementById(elemID);
    if (returnObj) {
      return returnObj;
    } else { return null }
  }
  hideElem = function (dElem, style='', isHide = true) {
    if (dElem) {
      visibility = (isHide == true ? 'none' : style);
      dElem.style.display = visibility;
    }
    return;
  }

  //first hide all error divs on page load
  searchQueryErr = getElem('searchQueryErr');
  stateNamesErr = getElem('stateNamesErr');
  wrapDisplay = 'none';

  const searchFld = getElem("id_searchQuery");

  //get selected searchType [ national, by_state, by_metro, by_county ]
  const ddlSearchType = getElem('id_searchType');
  var searchType = getElem('id_searchType').value;

  //hide loading graphic
  const loaderImg = getElem("loader-container");
  if (loaderImg) { hideElem(loaderImg); }


  const stateNamesWrapper = getElem("stateNamesWrapper");
  if (searchType != "by_state" && searchType != "by_county") {
    hideElem(stateNamesWrapper);
  }

  const metroNamesWrapper = getElem("metroNamesWrapper");
  if (searchType != "by_metro") {
    hideElem(metroNamesWrapper);
  }

  const countyNamesWrapper = getElem("countyNamesWrapper");
  if (searchType != "by_county") {
    hideElem(countyNamesWrapper);
  }


  var ddlStateNames = getElem('id_stateNames');
  var ddlCountyNames = getElem('id_countyNames');

  if(searchType == "by_county") {//technically this shouldn't happen
    if(ddlStateNames) {
      if(ddlStateNames.selectedValue == '0') {
        if(ddlCountyNames) {
          ddlCountyNames.disabled = true;
        }
      }
    } else {
      console.error("No stateNames dropdown list?...");
    }
  }


  //## SUBMIT BUTTON click event
  const submitBtn = getElem("submitBtn");
  submitBtn.addEventListener("click", function (evt) {
    try {
      evt.preventDefault();
      var submitForm = true;

      // values: national, by_state, by_metro, by_county
      if (ddlSearchType) {
        switch (ddlSearchType.value) {
          case 'by_county':
            console.log('CASE by_county');
            var ddlStateNames = getElem('id_stateNames');
            if (ddlStateNames) {
              submitForm = (ddlStateNames.value == '0') ? false : true;
              if (!submitForm) {
                hideElem(stateNamesErr, 'block', false);
              }
            }
            break;
        }
      }
    } catch (err) {
      console.error("Error in submitBtn.click()", err.message);
    } finally {
      if (searchFld.value == '') {
        hideElem(searchQueryErr, 'block', false);
        submitForm = false;
      }

      if (submitForm) {
        ddlCountyNames.disabled = false;
        getElem('churchesSearchForm').submit();
      }
      else {
        hideElem(loaderImg);
      }


    }
  });

  //## SEARCH TYPE change() event
  ddlSearchType.addEventListener("change", function (evt) {
    const selectedValue = evt.target.value;
    const lblStateNames = document.getElementById('lblStateNames');

    if(selectedValue == 'by_county') {
      lblStateNames.className = 'required';

      //also checking for stateName, if not selected, disable countNames ddl
      if(ddlStateNames) {
        if(ddlStateNames.value = '0') {
          if(ddlCountyNames) {
            ddlCountyNames.options[0].text = 'pick a state first';
            ddlCountyNames.disabled = true;
          }
        }
      } else {alert("test") } //pass
    } else {
      lblStateNames.className = '';
    }

    // BY STATE
    wrapDisplay = (selectedValue == 'by_state' || selectedValue == 'by_county' ? '' : 'none');
    ddlStateNames.selectedIndex = 0; //reset to 'select a state' between flips of ddl
    stateNamesWrapper.style.display = wrapDisplay;

    // BY METRO
    wrapDisplay = (selectedValue == 'by_metro' ? '' : 'none');
    metroNamesWrapper.style.display = wrapDisplay;

    // BY COUNTY
    wrapDisplay = (selectedValue == 'by_county' ? '' : 'none');
    countyNamesWrapper.style.display = wrapDisplay;
  });


  ddlStateNames.addEventListener("change", function (evt) {
    const selectedValue = evt.target.value;
    searchType = ddlSearchType.value;
    if(searchType == "by_county" && selectedValue != "0") {
      ddlCountyNames.options[0].text = "click 'submit'";
    }
  });


});//end DOMContentLoaded()