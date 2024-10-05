import ctypes
import ctypes.wintypes
import win32security
import win32process
import win32api
import pywintypes
from ctypes import windll, byref, create_unicode_buffer, Structure, Union, c_void_p, c_uint32, c_uint64
import logging
from common.logger import logger
import subprocess
import sys
import winreg

# Constants
INFINITE = 0xFFFFFFFF
ERROR_SUCCESS = 0
FWPM_ENGINE_OPTION_API_VERSION = 0
RPC_C_AUTHN_WINNT = 10
FWP_UINT32 = 0

# Structures
class FWP_VALUE0(Union):
    _fields_ = [
        ("uint32", ctypes.c_uint32),
        ("uint64", ctypes.c_uint64),
        ("float", ctypes.c_float),
        ("byteArray16", ctypes.c_byte * 16),
        ("byteBlob", c_void_p),
        ("sid", c_void_p),
        ("string", ctypes.wintypes.LPCWSTR),
        ("uint64Array", c_void_p),
        ("tokenInformation", c_void_p)
    ]

class FWPM_SESSION0(Structure):
    _fields_ = [
        ("sessionKey", ctypes.c_ubyte * 16),
        ("displayData", c_void_p),
        ("flags", ctypes.wintypes.DWORD),
        ("txnWaitTimeoutInMSec", ctypes.wintypes.DWORD),
        ("processId", ctypes.wintypes.DWORD),
        ("sid", ctypes.wintypes.LPCWSTR),
        ("username", ctypes.wintypes.LPCWSTR),
        ("kernelMode", ctypes.wintypes.BOOL)
    ]

class FWPM_FILTER0(Structure):
    _fields_ = [
        ("filterKey", ctypes.c_ubyte * 16),
        ("displayData", c_void_p),
        ("flags", ctypes.wintypes.DWORD),
        ("providerKey", ctypes.c_void_p),
        ("providerData", c_void_p),
        ("layerKey", ctypes.c_ubyte * 16),
        ("subLayerKey", ctypes.c_ubyte * 16),
        ("weight", FWP_VALUE0),
        ("numFilterConditions", ctypes.c_uint32),
        ("filterCondition", c_void_p),
        ("action", c_void_p),
        ("context", ctypes.c_ubyte * 16),
        ("providerContextKey", ctypes.c_ubyte * 16),
        ("reserved", ctypes.c_ubyte * 16),
        ("filterId", ctypes.c_uint64),
        ("effectiveWeight", FWP_VALUE0)
    ]

class WFPWrapper:
    def __init__(self):
        try:
            self.fwpuclnt = windll.LoadLibrary("fwpuclnt.dll")
            logger.info("Successfully loaded fwpuclnt.dll")
            
            # Verify essential functions exist
            required_functions = [
                'FwpmEngineOpen0', 'FwpmEngineClose0', 'FwpmEngineGetOption0',
                'FwpmFilterAdd0', 'FwpmFilterDeleteById0', 'FwpmFilterEnum0',
                'FwpmFilterCreateEnumHandle0', 'FwpmFilterDestroyEnumHandle0'
            ]
            for func in required_functions:
                if not hasattr(self.fwpuclnt, func):
                    raise AttributeError(f"{func} function not found in fwpuclnt.dll")
            
        except OSError as e:
            logger.error(f"Failed to load fwpuclnt.dll: {str(e)}")
            raise
        except AttributeError as e:
            logger.error(f"Invalid fwpuclnt.dll loaded: {str(e)}")
            raise

        self.engine_handle = ctypes.wintypes.HANDLE()
        self.session = FWPM_SESSION0()

        # Define argtypes and restype for functions
        self._define_function_prototypes()

    def _define_function_prototypes(self):
        # FwpmEngineOpen0
        self.fwpuclnt.FwpmEngineOpen0.argtypes = [
            ctypes.wintypes.LPCWSTR,
            ctypes.wintypes.DWORD,
            ctypes.c_void_p,
            ctypes.POINTER(FWPM_SESSION0),
            ctypes.POINTER(ctypes.wintypes.HANDLE)
        ]
        self.fwpuclnt.FwpmEngineOpen0.restype = ctypes.wintypes.DWORD

        # FwpmEngineGetOption0
        self.fwpuclnt.FwpmEngineGetOption0.argtypes = [
            ctypes.wintypes.HANDLE,
            ctypes.wintypes.DWORD,
            ctypes.POINTER(FWP_VALUE0)
        ]
        self.fwpuclnt.FwpmEngineGetOption0.restype = ctypes.wintypes.DWORD

        # FwpmFilterAdd0
        self.fwpuclnt.FwpmFilterAdd0.argtypes = [
            ctypes.wintypes.HANDLE,
            ctypes.POINTER(FWPM_FILTER0),
            ctypes.c_void_p,
            ctypes.POINTER(ctypes.c_uint64)
        ]
        self.fwpuclnt.FwpmFilterAdd0.restype = ctypes.wintypes.DWORD

        # FwpmFilterDeleteById0
        self.fwpuclnt.FwpmFilterDeleteById0.argtypes = [
            ctypes.wintypes.HANDLE,
            ctypes.c_uint64
        ]
        self.fwpuclnt.FwpmFilterDeleteById0.restype = ctypes.wintypes.DWORD

        # Add more function prototypes as needed

    def execute_command(self, func, *args):
        try:
            logger.info(f"Executing WFP function: {func.__name__}")
            result = func(*args)
            if result != ERROR_SUCCESS:
                error_msg = win32api.FormatMessage(result).strip()
                logger.error(f"WFP command {func.__name__} failed with error code {result}: {error_msg}")
                raise Exception(f"WFP command {func.__name__} failed with error code {result}: {error_msg}")
            return result
        except Exception as e:
            logger.error(f"WFP command {func.__name__} failed: {str(e)}")
            raise

    def initialize(self):
        self._check_environment()
        try:
            result = self.execute_command(
                self.fwpuclnt.FwpmEngineOpen0,
                None,
                ctypes.wintypes.DWORD(RPC_C_AUTHN_WINNT),
                None,
                ctypes.byref(self.session),
                ctypes.byref(self.engine_handle)
            )
            logger.info("WFP engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize WFP engine: {str(e)}")
            raise

        self._post_initialization_checks()

    def _check_environment(self):
        self._check_windows_version()
        self._check_bfe_service()
        self._check_windows_firewall()
        self._check_conflicting_software()
        self._check_wfp_dependencies()
        self._check_firewall_policy()

    def _check_windows_version(self):
        win_version = sys.getwindowsversion()
        if (win_version.major < 10) or (win_version.major == 10 and win_version.build < 19041):
            logger.error("WFP requires Windows 10 version 2004 (build 19041) or later.")
            raise Exception("Unsupported Windows version")
        logger.info(f"Windows version: {win_version.major}.{win_version.minor} Build {win_version.build}")

    def _check_bfe_service(self):
        result = subprocess.run(["sc", "query", "bfe"], capture_output=True, text=True)
        if "RUNNING" not in result.stdout:
            logger.error("Base Filtering Engine service is not running.")
            raise Exception("Base Filtering Engine service must be running for WFP operations.")
        logger.info("Base Filtering Engine service is running.")

    def _check_windows_firewall(self):
        result = subprocess.run(["sc", "query", "MpsSvc"], capture_output=True, text=True)
        if "RUNNING" not in result.stdout:
            logger.warning("Windows Firewall service is not running. This may affect WFP operations.")
        else:
            logger.info("Windows Firewall service is running.")

    def _check_conflicting_software(self):
        conflicting_processes = ["antivirus.exe", "thirdpartyfirewall.exe"]  # Add known conflicting processes
        for process in conflicting_processes:
            result = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {process}"], capture_output=True, text=True)
            if process.lower() in result.stdout.lower():
                logger.warning(f"Potentially conflicting software detected: {process}")

    def _check_wfp_dependencies(self):
        dependencies = ["BFE", "RpcSs", "WinHttpAutoProxySvc"]
        for dep in dependencies:
            result = subprocess.run(["sc", "query", dep], capture_output=True, text=True)
            if "RUNNING" not in result.stdout:
                logger.error(f"Required service {dep} is not running.")
                raise Exception(f"Required service {dep} is not running")

    def _check_firewall_policy(self):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy") as key:
                value, _ = winreg.QueryValueEx(key, "EnableFirewall")
                if value == 0:
                    logger.warning("Windows Firewall is disabled by policy. This may affect WFP operations.")
                else:
                    logger.info("Windows Firewall policy check passed.")
        except Exception as e:
            logger.error(f"Error checking Windows Firewall policy: {str(e)}")

    def _post_initialization_checks(self):
        self._check_wfp_version()
        self._check_wfp_state()
        self._test_wfp_connection()

    def _check_wfp_version(self):
        try:
            version = FWP_VALUE0()
            version.uint32 = 0
            result = self.execute_command(
                self.fwpuclnt.FwpmEngineGetOption0,
                self.engine_handle,
                ctypes.wintypes.DWORD(FWPM_ENGINE_OPTION_API_VERSION),
                ctypes.byref(version)
            )
            logger.info(f"WFP API version: {version.uint32}")
        except Exception as e:
            logger.error(f"Error checking WFP version: {str(e)}")

    def _check_wfp_state(self):
        try:
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\BFE") as key:
                start, _ = winreg.QueryValueEx(key, "Start")
                if start != 2:  # 2 means AUTO_START
                    logger.warning("Base Filtering Engine service is not set to start automatically.")
                else:
                    logger.info("Base Filtering Engine service is set to start automatically.")
        except Exception as e:
            logger.error(f"Error checking BFE service state: {str(e)}")

    def _test_wfp_connection(self):
        try:
            option = FWP_VALUE0()
            option.uint32 = 0
            result = self.execute_command(
                self.fwpuclnt.FwpmEngineGetOption0,
                self.engine_handle,
                ctypes.wintypes.DWORD(FWPM_ENGINE_OPTION_API_VERSION),
                ctypes.byref(option)
            )
            logger.info("Basic WFP test succeeded")
        except Exception as e:
            logger.error(f"Basic WFP test failed: {str(e)}")

    def add_rule(self, rule):
        logger.info(f"Adding rule: {rule}")
        try:
            # Create a FWPM_FILTER0 structure and populate it with rule details
            filter = FWPM_FILTER0()
            # Populate filter structure with rule details
            # This is a placeholder and needs to be implemented based on the rule structure
            filter_id = ctypes.c_uint64()
            result = self.execute_command(
                self.fwpuclnt.FwpmFilterAdd0,
                self.engine_handle,
                ctypes.byref(filter),
                None,
                ctypes.byref(filter_id)
            )
            logger.info(f"Rule added successfully. Filter ID: {filter_id.value}")
            return filter_id.value
        except Exception as e:
            logger.error(f"Failed to add rule: {str(e)}")
            raise

    def delete_rule(self, filter_id):
        try:
            self.execute_command(
                self.fwpuclnt.FwpmFilterDeleteById0,
                self.engine_handle,
                c_uint64(filter_id)
            )
            logger.info(f"Deleted rule with ID {filter_id}")
        except Exception as e:
            logger.error(f"Failed to delete rule with ID {filter_id}: {str(e)}")
            raise

    def list_rules(self):
        logger.info("Listing all rules")
        # This is a placeholder. Implement FwpmFilterEnum0 to list all filters
        pass

    def update_rule(self, old_rule_id, new_rule):
        try:
            self.delete_rule(old_rule_id)
            new_rule_id = self.add_rule(new_rule)
            logger.info(f"Updated rule: {old_rule_id} -> {new_rule_id}")
            return new_rule_id
        except Exception as e:
            logger.error(f"Failed to update rule from {old_rule_id} to {new_rule}: {str(e)}")
            raise

    def flush_rules(self):
        logger.info("Flushing all rules")
        # This is a placeholder. Implement logic to remove all filters
        pass

    def delete_all_rules(self):
        logger.info("Deleting all rules and associated structures")
        # This is a placeholder. Implement logic to remove all filters and associated structures
        pass

    def add_app_specific_rule(self, app_name, pid, allowed_ports):
        logger.info(f"Adding app-specific rule for {app_name} (PID: {pid}) on ports {allowed_ports}")
        try:
            for port in allowed_ports:
                # Create a FWPM_FILTER0 structure for the app-specific rule
                filter = FWPM_FILTER0()
                # Populate filter structure with app-specific details
                # This is a placeholder and needs to be implemented based on WFP specifics
                filter_id = ctypes.c_uint64()
                result = self.execute_command(
                    self.fwpuclnt.FwpmFilterAdd0,
                    self.engine_handle,
                    ctypes.byref(filter),
                    None,
                    ctypes.byref(filter_id)
                )
                logger.info(f"App-specific rule added for {app_name} on port {port}. Filter ID: {filter_id.value}")
        except Exception as e:
            logger.error(f"Failed to add app-specific rule for {app_name}: {str(e)}")
            raise

    def get_default_policy(self):
        logger.info("Getting default filter (equivalent to chain policy)")
        try:
            # This is a placeholder. Implement logic to get the default filter
            # You may need to use FwpmNetEventsGetSecurityInfo0 or similar function
            return "ALLOW"  # Default placeholder return
        except Exception as e:
            logger.error(f"Failed to get default policy: {str(e)}")
            raise

    def set_default_policy(self, policy):
        logger.info(f"Setting default filter (equivalent to chain policy) to: {policy}")
        try:
            # This is a placeholder. Implement logic to set the default filter
            # You may need to use FwpmNetEventsSetSecurityInfo0 or similar function
            pass
        except Exception as e:
            logger.error(f"Failed to set default policy to {policy}: {str(e)}")
            raise

    def cleanup(self):
        if self.engine_handle:
            try:
                self.fwpuclnt.FwpmEngineClose0(self.engine_handle)
                logger.info("WFP engine closed")
            except Exception as e:
                logger.error(f"Failed to close WFP engine: {str(e)}")
            finally:
                self.engine_handle = ctypes.wintypes.HANDLE()
        else:
            logger.info("WFP engine handle was not initialized. No need to close.")

    def __enter__(self):
        self.initialize()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()
        if exc_type:
            logger.error(f"Exception occurred: {exc_type.__name__}: {exc_val}")
            return False  # Propagate the exception
        return True

def run_as_admin():
    if 'asadmin' not in sys.argv:
        try:
            import win32com.shell.shell as shell
        except ImportError:
            logger.error("pywin32 is required for administrative privileges. Please install it via 'pip install pywin32'.")
            sys.exit(1)
        script = sys.argv[0]
        params = ' '.join([script] + sys.argv[1:] + ['asadmin'])
        try:
            shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
            sys.exit()
        except Exception as e:
            logger.error(f"Failed to elevate to administrator: {str(e)}")
            sys.exit(1)
    else:
        try:
            is_admin = win32security.IsUserAnAdmin()
        except:
            is_admin = False
        if not is_admin:
            print("Script is not running with admin rights. Please run as administrator.")
            sys.exit(1)

if __name__ == "__main__":
    run_as_admin()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger.info("Starting Windows Firewall Agent")
    
    with WFPWrapper() as wfp:
        try:
            # Your main logic here
            # Example:
            # rule = {...}  # Define your rule structure
            # wfp.add_rule(rule)
            pass
        except Exception as e:
            logger.error(f"Error in main execution: {e}")

    logger.info("Windows Firewall Agent stopped")