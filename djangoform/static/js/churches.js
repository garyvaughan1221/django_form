
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

  //get selected searchType [ national, by_state, by_metro, by_county ]
  const searchType = getElem('id_searchType').value;
  wrapDisplay = 'none';

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
  if (searchType != 'by_county') {
    hideElem(countyNamesWrapper);
  }


  // cannot submit form with empty search field, otherwise show loader img
  const submitBtn = getElem("submitBtn");
  const searchFld = getElem("id_searchQuery");
  submitBtn.addEventListener("click", function (evt) {
    try {
      evt.preventDefault();
      var submitForm = true;

      var ddlSearchType = getElem('id_searchType');
      if (ddlSearchType) {
        switch (ddlSearchType.value) {
          case 'by_county':
            console.log('CASE by_county');
            var ddlStateNames = getElem('id_stateNames');
            if (ddlStateNames) {
              submitForm = (ddlStateNames.value == '0') ? false : true;
              if(!submitForm) {
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

      if (submitForm) { getElem('churchesSearchForm').submit(); }
      else {
        hideElem(loaderImg);
      }


    }
  });

  // change() event for searchType dropdown list
  const ddlSearchType = getElem("id_searchType");
  ddlSearchType.addEventListener("change", function (evt) {
    const selectedValue = evt.target.value;
    const lblStateNames = document.getElementById('lblStateNames');

    if(selectedValue == 'by_county') {
      lblStateNames.className = 'required';
    } else {
      lblStateNames.className = '';
    }

    // BY STATE
    wrapDisplay = (selectedValue == 'by_state' || selectedValue == 'by_county' ? '' : 'none');
    const stateNames = getElem('id_stateNames');
    stateNames.selectedIndex = 0; //reset to 'select a state' between flips of ddl

    stateNamesWrapper.style.display = wrapDisplay;


    // BY METRO
    wrapDisplay = (selectedValue == 'by_metro' ? '' : 'none');
    metroNamesWrapper.style.display = wrapDisplay;

    // BY COUNTY
    wrapDisplay = (selectedValue == 'by_county' ? '' : 'none');
    countyNamesWrapper.style.display = wrapDisplay;
  });
});