; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define NSSM "nssm.exe"
#define AmonServiceName "AmonAgent"
#define AmonApp "amon-agent.exe"


[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{33541FBB-1B7C-4C64-8902-420ACE513DF9}
AppName=amon-agent
AppVersion=1.3.1
;AppVerName=amon-agent 1.0
AppPublisher=Simplistic LLC
AppPublisherURL=https://amon.cx
AppSupportURL=https://amon.cx
AppUpdatesURL=https://amon.cx
DefaultDirName={pf}\AmonAgent
DefaultGroupName=amon-agent
OutputBaseFilename=amon-agent-1.3.1
Compression=lzma
SolidCompression=yes
WizardImageFile=welcome.bmp
DisableDirPage=auto
DisableProgramGroupPage=yes
CloseApplications=yes
RestartApplications=yes
AlwaysRestart=no
UninstallDisplayIcon={app}\amon-agent.exe
PrivilegesRequired=admin

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\amon-agent.exe"; DestDir: "{app}"; Flags: ignoreversion restartreplace;
; NOTE: Don't use "Flags: ignoreversion" on any shared system files
Source: "nssm.exe"; DestDir: "{app}"
Source: "amon-agent.ini"; DestDir: "{app}"; Permissions: everyone-full;

[INI]
Filename: {app}\amon-agent.ini; Section: Main; Key: amon_url; String: {code:GetAmonUrl}
Filename: {app}\amon-agent.ini; Section: Main; Key: server_key; String: {code:GetKey}

[Icons]
Name: "{group}\amon-agent"; Filename: "{app}\amon-agent.exe"



[Run]
; post-install
Filename: "{sys}\msiexec.exe"; Parameters: "/package ""{app}\{#AmonApp}"" /qn /norestart /nocloseapplications /passive"; Flags: shellexec waituntilterminated;
Filename: "{sys}\netsh.exe"; Parameters: "advfirewall firewall add rule name=""AmonAgent Out"" program=""{app}\{#AmonApp}"" dir=out action=allow enable=yes"; Flags: runhidden;
Filename: "{app}\{#NSSM}"; Parameters: "install {#AmonServiceName} ""{app}\{#AmonApp}"" "; Flags: runhidden;
Filename: "{app}\{#NSSM}"; Parameters: "set {#AmonServiceName} AppDirectory {app}"; Flags: runhidden;
Filename: "{app}\{#NSSM}"; Parameters: "set {#AmonServiceName} AppStdout {userappdata}\Amon\amon.log"; Flags: runhidden;
Filename: "{app}\{#NSSM}"; Parameters: "set {#AmonServiceName} AppStderr {userappdata}\Amon\amon.log"; Flags: runhidden;
Filename: "{app}\{#NSSM}"; Parameters: "start {#AmonServiceName}"; Flags: runhidden;


[UninstallDelete]
Type: filesandordirs; Name: "{app}"


[UninstallRun]
; pre-uninstall
Filename: "{app}\{#NSSM}"; Parameters: "stop {#AmonServiceName}"; Flags: runhidden;
Filename: "{app}\{#NSSM}"; Parameters: "remove {#AmonServiceName} confirm"; Flags: runhidden;

[InstallDelete]
Type: files; Name: "{app}\amon-agent.exe"

[Code]
var
  UserPage: TInputQueryWizardPage;
  
procedure InitializeWizard;
begin
  { Create the pages }
  UserPage := CreateInputQueryPage(wpWelcome,
    'Amon Information', '',
    'Please specify the URL where your Amon instance is running and the agent server key, then click Next.');
  UserPage.Add('Amon URL:', False);
  UserPage.Add('Server Key:', False);

UserPage.Values[0] := GetIniString('Main', 'amon_url', '', WizardDirValue + '\amon-agent.ini');
UserPage.Values[1] := GetIniString('Main', 'server_key', '', WizardDirValue + '\amon-agent.ini');
end;

function GetAmonUrl(Param: String): string;
begin
result := UserPage.Values[0];
end;

function GetKey(Param: String): string;
begin
result := UserPage.Values[1];
end;


function GetUninstallString: string;
var
  sUnInstPath: string;
  sUnInstallString: String;
begin
  Result := '';
  sUnInstPath := ExpandConstant('Software\Microsoft\Windows\CurrentVersion\Uninstall\33541FBB-1B7C-4C64-8902-420ACE513DF9_is1'); //Your App GUID/ID
  sUnInstallString := '';
  if not RegQueryStringValue(HKLM, sUnInstPath, 'UninstallString', sUnInstallString) then
    RegQueryStringValue(HKCU, sUnInstPath, 'UninstallString', sUnInstallString);
  Result := sUnInstallString;
end;

function IsUpgrade: Boolean;
begin
  Result := (GetUninstallString() <> '');
end;

function InitializeSetup: Boolean;
var
  V: Integer;
  iResultCode: Integer;
  sUnInstallString: string;
begin
  Result := True; // in case when no previous version is found
  if RegValueExists(HKEY_LOCAL_MACHINE,'Software\Microsoft\Windows\CurrentVersion\Uninstall\33541FBB-1B7C-4C64-8902-420ACE513DF9_is1', 'UninstallString') then  //Your App GUID/ID
  begin
    V := MsgBox(ExpandConstant('An old version of the Amon Agent was detected. Do you want to uninstall it?'), mbInformation, MB_YESNO); //Custom Message if App installed
    if V = IDYES then
    begin
      sUnInstallString := GetUninstallString();
      sUnInstallString :=  RemoveQuotes(sUnInstallString);
      Exec(ExpandConstant(sUnInstallString), '', '', SW_SHOW, ewWaitUntilTerminated, iResultCode);
      Result := True; //if you want to proceed after uninstall
                //Exit; //if you want to quit after uninstall
    end
    else
      Result := False; //when older version present and not uninstalled
  end;
end;