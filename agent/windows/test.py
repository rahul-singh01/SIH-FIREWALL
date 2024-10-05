import ctypes
import ctypes.wintypes
import win32api

def test_wfp_api():
    try:
        # Load the WFP library
        fwpuclnt = ctypes.windll.LoadLibrary("fwpuclnt.dll")
        print("Successfully loaded fwpuclnt.dll")

        # Check if specific functions exist
        functions_to_check = [
            "FwpmEngineOpen0",
            "FwpmEngineClose0",
            "FwpmGetAppIdFromFileName0",
            "FwpmFilterAdd0",
            "FwpmFilterDeleteById0"
        ]

        for func_name in functions_to_check:
            if hasattr(fwpuclnt, func_name):
                print(f"Function {func_name} exists")
            else:
                print(f"Function {func_name} does not exist")

        # Try to open the WFP engine
        engine_handle = ctypes.wintypes.HANDLE()
        result = fwpuclnt.FwpmEngineOpen0(
            None,
            ctypes.c_uint32(0),  # RPC_C_AUTHN_WINNT
            None,
            None,
            ctypes.byref(engine_handle)
        )

        if result == 0:  # ERROR_SUCCESS
            print("Successfully opened WFP engine")
            fwpuclnt.FwpmEngineClose0(engine_handle)
            print("Successfully closed WFP engine")
        else:
            error_msg = win32api.FormatMessage(result)
            print(f"Failed to open WFP engine. Error code: {result}, Message: {error_msg}")

            # Try to get more information about the error
            last_error = ctypes.get_last_error()
            if last_error:
                error_msg = win32api.FormatMessage(last_error)
                print(f"Last error: {last_error}, Message: {error_msg}")

    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    test_wfp_api()