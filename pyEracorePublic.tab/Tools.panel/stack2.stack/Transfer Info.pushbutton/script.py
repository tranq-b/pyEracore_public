__title__ = "Transfer Info"

from my_lib.import_all import *

# specify the file path
file_path_folder = os.path.join(os.path.expanduser("~"), ".cache", "RevitPlugin", "MyPy")

if not os.path.exists(file_path_folder):
    os.makedirs(file_path_folder)

    file_path = os.path.join(file_path_folder, "SetParameters.txt")

# res = forms.alert("Which way calculating should use?",
#                   options=["Select parameters",
#                            "Load parameters"
#                            ])
#
# res1 = forms.alert("Selection Option",
#                   options=["Single Element Start and Multi-Element Finish",
#                            "Repeated Element Selection Until ESC"
#                            ])
selected_option, switches = \
    forms.CommandSwitchWindow.show(
        ['Select parameters', 'Load parameters', 'Cancel'],
        switches=['Repeated Element', "Fill In"],
        message='Select Option:',
        recognize_access_key=True
    )

if selected_option != "Cancel":


    element1 = revit.pick_element(message="Pick First Element")



    if selected_option == "Select parameters":
        parameters_list = []
        for parameter in element1.Parameters:
            parameters_list.append(parameter.Definition.Name)
        parameters_list = sorted(parameters_list)
        get_parameter = forms.SelectFromList.show(parameters_list, button_name='Get Parameter', multiselect=True)


        # check if the file exists
        if os.path.isfile(file_path):
            # file exists, open it in append mode
            file = open(file_path, "w")
            file.close()
            file = open(file_path, "a+")
        else:
            # file doesn't exist, create it
            file = open(file_path, "w")

        # write the list to the file
        file.write(str(get_parameter))

        # close the file
        file.close()

    else:
        file = open(file_path, "r")
        get_parameter = file.read()
        get_parameter = ast.literal_eval(get_parameter)
        file.close()




    # Start a transaction
    if not switches["Repeated Element"]:
        t = Transaction(doc, 'TI')
        t.Start()
        try:
            elements = revit.pick_elements()
            for parameter in get_parameter:
                set_parameter = Element.LookupParameter(element1, parameter)
                for element in elements:
                    try:
                        if str(set_parameter.StorageType) == "String":
                            Element.LookupParameter(element, parameter).Set(set_parameter.AsString())
                        elif str(set_parameter.StorageType) == "Double":
                            Element.LookupParameter(element, parameter).Set(set_parameter.AsDouble())
                        elif str(set_parameter.StorageType) == "Integer":
                            Element.LookupParameter(element, parameter).Set(set_parameter.AsInteger())
                    except:
                        pass

            # Commit the transaction
            t.Commit()

        except Exception as e:
            # If an exception occurs, roll back the transaction
            t.RollBack()
            print(e)

    else:
        green = Color(0, 255, 0)
        done_elements = [element1]
        try:
            while element1:
                t = Transaction(doc, 'TI1')
                t.Start()
                try:
                    second_element = revit.pick_element(message="Pick second element")
                    done_elements.append(second_element)
                    for parameter in get_parameter:
                        set_parameter = Element.LookupParameter(element1, parameter)
                        element = second_element
                        if switches["Fill In"]:
                            run = sort_to_runs([element])
                            for element in run[0]:
                                try:
                                    if str(set_parameter.StorageType) == "String":
                                        Element.LookupParameter(element, parameter).Set(set_parameter.AsString())
                                    elif str(set_parameter.StorageType) == "Double":
                                        Element.LookupParameter(element, parameter).Set(set_parameter.AsDouble())
                                    elif str(set_parameter.StorageType) == "Integer":
                                        Element.LookupParameter(element, parameter).Set(set_parameter.AsInteger())
                                except:
                                    pass
                        else:
                            try:
                                if str(set_parameter.StorageType) == "String":
                                    Element.LookupParameter(element, parameter).Set(set_parameter.AsString())
                                elif str(set_parameter.StorageType) == "Double":
                                    Element.LookupParameter(element, parameter).Set(set_parameter.AsDouble())
                                elif str(set_parameter.StorageType) == "Integer":
                                    Element.LookupParameter(element, parameter).Set(set_parameter.AsInteger())
                            except:
                                pass
                    Override([element1], green)
                    Override([second_element], green)
                    update_model()
                    element1 = revit.pick_element(message="Pick First Element")
                    if not element1:
                        overrides = OverrideGraphicSettings()
                        for i in done_elements:
                            doc.ActiveView.SetElementOverrides(i.Id, overrides)
                    else:
                        done_elements.append(element1)

                    # Commit the transaction
                    t.Commit()


                except Exception as e:
                    tb_str = traceback.format_exc()
                    print("IronPython Traceback:")
                    print(tb_str)
        except:
            pass
