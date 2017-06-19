/**
 * Created by Manuel on 15/05/2017.
 */

RodiApp.controller('RodiCtrl', ['$scope', 'RodiSrv', '$window', '$filter', '$cookieStore', '$location', function ($scope, RodiSrv, $window, $filter, $cookieStore, $location) {

    // ************************************** //
    // *************** INIT ***************** //
    // ************************************** //

    $scope.bLogin = false;
    $scope.tokenid = $cookieStore.get('rodi_token');
    $scope.userinfo = $cookieStore.get('rodi_user');

    if($scope.tokenid) {$scope.bLogin = true; } else {$scope.bLogin = false;}

    $scope.objRodiVariable =
        {
            "valueData": "",
            "countryID": "",
            "countryDesc": "",
            "bPopupCountry": false,
            "popupClass": "",
            "popupX": "",
            "popupY": "",
            "location": baseUrl
        };

    // Hazard Filters
    $scope.objHazardFilters =
        {
            "filterRiverFlood": "",
            "filterEarthquake": "",
            "filterVolcano": "",
            "filterCyclone": "",
            "filterCoastalFlood": "",
            "filterWaterScarsity": "",
            "filterLandSlide": "",
            "filterTsunami": ""
        };

    // Chiamo il service per compilare l'arrayData
    $scope.arrayData = RodiSrv.getMapScores($scope.objHazardFilters);

    // Chiamo il servizio per le news
    $scope.news = RodiSrv.getNewsList(4);

    $scope.changepage = function(page)
    {
        $window.location.href = baseUrl + page;
    }

    // ************************************** //
    // ************* FILTERS **************** //
    // ************************************** //

    // Setto i filtri attivi
    $scope.setFilter = function(elementKey)
    {
        if ($scope.objHazardFilters[elementKey] !== ''){
            $scope.objHazardFilters[elementKey] = "";
        } else {
            $scope.objHazardFilters[elementKey] = "active";
        }

    };

    // ************************************** //
    // ************* MATRIX ***************** //
    // ************************************** //

    if ($location.path().indexOf('browse-data.html') !== -1)
    {
        // Get the Hazard Category
        $scope.HazardCategory = [];
        RodiSrv.getHazardCategory($scope.tokenid,
            function(data){
                // Success
                $scope.HazardCategory = data;
            }, function(data){
                //Error
            });

        $scope.matrixData = RodiSrv.getMatrixData($scope.objHazardFilters);

        $scope.getHCIcon = function(index)
        {
            return RodiSrv.getHCIcon(index - 1);
        };

        $scope.colorCell = function(value){
            return RodiSrv.matrixColorCell(value);
        }
    }



    // ************************************** //
    // ********* CONTRIBUTE PAGE ************ //
    // ************************************** //


    if ($location.path().indexOf('contribute.html') !== -1){

        $scope.tab = 0;

        $scope.objDataset = RodiSrv.getDatasetEmptyStructure();
        // $scope.objDatasetClass = RodiSrv.getDatasetClassification();

        // Get the Hazard Category
        $scope.HazardCategory = [];
        $scope.DatasetName = [];
        RodiSrv.getHazardCategory($scope.tokenid,
            function(data){
                // Success
                $scope.HazardCategory = data;

            }, function(data){
                //Error
                $scope.HazardCategory = ["Error loading Category"];
        });

        $scope.setDatasetName = function(hcId)
        {
            console.log(hcId);
            RodiSrv.getDatasetName(hcId,
                function(data){
                    // Success
                    $scope.DatasetName = data;
                    console.log(data);

                    // Description
                    RodiSrv.getDatasetDescription(hcId, 1,
                        function(data){
                            // Success
                            console.log(data);

                            RodiSrv.getDatasetResolution(hcId, 1,1,
                                function(data){
                                    // Success
                                    console.log(data);
                                }, function(data){
                                    // Error
                                    console.log(data);
                                })

                        }, function(data){
                            // Error
                            console.log(data);
                        })


                }, function(data){
                    // Error
                    $scope.DatasetName = ["Error loading Dataset name"];
                })
        }

        RodiSrv.getCountryList(
            function(data){
                // Success
                $scope.countryList = data;
            }, function(data){
                // Error
                // TODO: error message
            });

        // $scope.hazardList = RodiSrv.getHazardList();
        $scope.questions = RodiSrv.getQuestions();
        $scope.objResolutionList = [];
        $scope.bResolutionDisable = true;

        $scope.filterDatasetResolution = function()
        {
            var aFilter = [];
            if($scope.objDataset.dataset_type != '--')
            {
                // hazard category selected
                aFilter = $filter('filter')($scope.objDatasetClass, {code: $scope.objDataset.dataset_type});

                if (!angular.equals({}, aFilter[0].level))
                {
                    // Resolution found
                    $scope.objResolutionList = aFilter[0].level;
                    $scope.bResolutionDisable = false;
                } else {
                    $scope.bResolutionDisable = true;
                }
            }
        }

        $scope.saveSelection = function(qcode, value)
        {
            var iIndex = 0;
            var foundItem = $filter('filter')($scope.objDataset.questions, {code: qcode});

            iIndex = $scope.objDataset.questions.indexOf(foundItem[0]);
            $scope.objDataset.questions[iIndex].value = value;

        }

        $scope.saveDataser = function()
        {

            var objQuestLost = [];
            var aErrorsValidation = [];

            // Validate Dataset structure
            aErrorsValidation = RodiSrv.validateDataset($scope.objDataset);

            if(aErrorsValidation.length > 0) {
                // Errors
                var strMsg = "Required fields: <ul>";
                for(var i=0; i< aErrorsValidation.length; i++)
                {
                    strMsg += '<li>' + aErrorsValidation[i] + '</li> ';
                }

                strMsg += "</ul>";
                vex.dialog.alert(strMsg);

            } else {
                // Save the dataser
                vex.dialog.alert('Under construction');
            }


            /*
             Save ***TODO***
             usr_ins
             data_ins
             */

            // var bMsh = RodiSrv.saveDataset($scope.objDataset);
            //
            // if (bMsh)
            // {
            //    Save success message
            //     vex.dialog.alert('Dataset Inserted correctly');
            //     $scope.objDataset = RodiSrv.getDatasetEmptyStructure();
            // } else
            // {
            //    Save error message
            // vex.dialog.alert('Error: dataser not insert!');
            // }
        }

        // ************************************** //
        // ****** USER PROFILE & DATA *********** //
        // ************************************** //

        $scope.$watch('bLogin', function() {

            if ($scope.bLogin){
                $scope.tokenid = $cookieStore.get('rodi_token');
                $scope.userinfo = $cookieStore.get('rodi_user');
            }

            // ************************************** //
            // ********** ADMIN FUNCTIONS *********** //
            // ************************************** //

            if ($scope.bLogin && $scope.userinfo.groups[0] == 'admin')
            {

                $scope.usradmininfo = RodiSrv.getUserStructureEmpty();
                $scope.usrRegList = [];
                $scope.stypeModal = "";
                $scope.groupSelect = null;

                RodiSrv.getUsersList($scope.tokenid,
                    function(data){
                        //Success
                        $scope.usrRegList = data;

                        $scope.openPopup = function (pk)
                        {

                            if(pk == -999)
                            {
                                // New user
                                $scope.stypeModal = "insert new profile";
                                $scope.usradmininfo = RodiSrv.getUserStructureEmpty();

                            } else {
                                // Edit user profile
                                var aUserProfile = $filter('filter')($scope.usrRegList, {pk: pk});
                                $scope.usradmininfo = aUserProfile[0];

                                if($scope.usradmininfo.groups.length == 0){
                                    $scope.groupSelect = 'normal';
                                } else {
                                    $scope.groupSelect = $scope.usradmininfo.groups[0];
                                }

                                $scope.stypeModal = "edit";
                            }


                            $('#editUser').modal('show');
                        }

                        $scope.saveUsrInfoAdmin = function()
                        {

                            if($scope.groupSelect == 'admin')
                            {
                                $scope.usradmininfo.is_staff = true;
                            }
                            else {
                                $scope.usradmininfo.is_staff = false;
                            }

                            if($scope.groupSelect == 'normal'){
                                $scope.usradmininfo.groups = [];
                            } else {
                                $scope.usradmininfo.groups[0] = $scope.groupSelect;
                            }

                            if($scope.usradmininfo.pk == -999)
                            {
                                // New user

                                RodiSrv.insertUserInfo($scope.tokenid, $scope.usradmininfo,
                                    function(data){
                                        // Success
                                        vex.dialog.alert('User info saved successfully');

                                        $scope.usrRegList.push($scope.usradmininfo);

                                        RodiSrv.getUsersList($scope.tokenid,
                                            function(data){
                                                // Success
                                                $scope.usrRegList = data;
                                            }, function(data){
                                                // Error
                                            })

                                    }, function(data){
                                        // Error
                                        vex.dialog.alert('Error: unable to save data');
                                    })

                            } else {
                                // Edit User profile

                                RodiSrv.saveUserInfo($scope.tokenid, $scope.usradmininfo,
                                    function(data){
                                        // Success
                                        vex.dialog.alert('User info saved successfully');
                                    }, function(data){
                                        // Error
                                        vex.dialog.alert('Error: unable to save data');
                                    }
                                )
                            }
                        }

                        $scope.deleteUsrInfoAdmin = function(pk)
                        {
                            vex.dialog.confirm({
                                message: 'Are you absolutely sure you want to delete this user profile?',
                                callback: function (value) {
                                    if(value)
                                    {
                                        // Delete profile
                                        RodiSrv.deleteUserInfo($scope.tokenid, pk,
                                            function(data){
                                                // Success

                                                // Reload data from server
                                                RodiSrv.getUsersList($scope.tokenid,
                                                    function(data){
                                                        // Success
                                                        $scope.usrRegList = data;
                                                    }, function(data){
                                                        // Error
                                                    })

                                            }, function(data){
                                                // Error
                                                vex.dialog.alert('Error: unable to delete data');
                                            })
                                    }
                                }
                            })
                        }

                    }, function(data){
                        // Error
                        // Fai nulla
                    }
                );

                // Profile dataset list
                $scope.bDatasetProfile = false;
                RodiSrv.getProfileDataset($scope.tokenid,
                    function(data){
                        // Success
                        if (data.length > 0)
                        {
                            $scope.bDatasetProfile = true;
                        } else {$scope.bDatasetProfile = false;}

                    }, function(data){
                        // Error
                        $scope.bDatasetProfile = false;
                    })
            }

            // ************************************** //
            // ********* ALL USER FUNCTIONS ********* //
            // ************************************** //
            if ($scope.bLogin)
            {
                // Profile dataset list
                $scope.bDatasetProfile = false;
                RodiSrv.getProfileDataset($scope.tokenid,
                    function(data){
                        // Success
                        if (data.length > 0)
                        {
                            $scope.bDatasetProfile = true;
                        } else {$scope.bDatasetProfile = false;}

                        console.log(data);
                    }, function(data){
                        // Error
                        $scope.bDatasetProfile = false;
                    })
            }

            // ************************************** //
            // ******* REVIEWER USER FUNCTIONS ****** //
            // ************************************** //
            if ($scope.bLogin && $scope.userinfo.groups[0] == 'reviewer'){

            }
        });

        $scope.putProfile = function()
        {
            // Save new profile data

            RodiSrv.saveProfile($scope.tokenid, $scope.userinfo,
                function(data){
                    //Success
                    vex.dialog.alert('Profile saved successfully');
                }, function(data){
                    // Error
                    vex.dialog.alert('Error: unable to save data');
                }
            );
        }

        $scope.resetProfilePsw = function(old_psw, new_psw, confirm_psw)
        {
            // Resetto la password per il profilo

            if(old_psw != '' && new_psw != ''){
                // All fileds are compiled
                if(confirm_psw == new_psw)
                {
                    // New password e confirm password corrisponded
                    RodiSrv.resetProfilePsw($scope.tokenid, old_psw, new_psw,
                        function(data){
                            // Success
                            console.log(data);
                            vex.dialog.alert('Password update!');
                        }, function(data){
                            // Error
                            var sMsg = "";
                            angular.forEach(data, function(value, key) {
                                sMsg = key.replace("_"," ") + ': ' + value
                                vex.dialog.alert(sMsg);
                            });

                        })

                } else {
                    vex.dialog.alert('Error: New password and password confirmation are not the same');
                }
            } else {
                vex.dialog.alert('Error: You must insert old password, new password and confirm the new password');
            }
        }

    }


    // ************************************** //
    // ****** DATASET LIST & DETAILS ******** //
    // ************************************** //

    if ($location.path().indexOf('dataset_list.html') !== -1)
    {
        // Dataset page
        $scope.idCountry = $location.search().idcountry;
        $scope.idHazCat = $location.search().idcategory;

        RodiSrv.getCountryList(
            function(data){
                // Success
                $scope.countryList = data;

                $scope.HazardCategory = [];
                RodiSrv.getHazardCategory($scope.tokenid,
                    function(data){
                        // Success
                        $scope.HazardCategory = data;
                        console.log($scope.HazardCategory);

                        $scope.HazardCategory = $filter('filter')($scope.HazardCategory, function(e){
                            return e.category.id == $scope.idHazCat;
                        });
                        console.log($scope.HazardCategory);

                    }, function(data){
                        //Error
                    });

                $scope.objCountry = $filter('filter')($scope.countryList, {iso2: $scope.idCountry});


            }, function(data){
                // Error
                // TODO: error message
        });



    }

} ]);
