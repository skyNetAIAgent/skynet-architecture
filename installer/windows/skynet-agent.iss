[Setup]
AppId=SkyNetResearchAgent
AppName=SkyNet Agent
AppVersion={#AgentVersion}
VersionInfoVersion={#AgentVersion}.0
DefaultDirName={localappdata}\SkyNetAgent
DisableDirPage=yes
UsePreviousAppDir=no
DefaultGroupName=SkyNet Agent
DisableProgramGroupPage=yes
PrivilegesRequired=lowest
ArchitecturesAllowed={#TargetArch}
ArchitecturesInstallIn64BitMode={#TargetArch}
OutputDir={#BuildDir}\dist
OutputBaseFilename=SkyNetAgentSetup-{#AgentVersion}-{#AssetArch}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
RestartApplications=no
UsePreviousTasks=no
UninstallDisplayName=SkyNet Agent

[Languages]
Name: "en"; MessagesFile: "compiler:Default.isl"
#if FileExists(AddBackslash(CompilerPath) + "Languages\ChineseSimplified.isl")
Name: "zh"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"
#elif FileExists(AddBackslash(CompilerPath) + "Languages\Unofficial\ChineseSimplified.isl")
Name: "zh"; MessagesFile: "compiler:Languages\Unofficial\ChineseSimplified.isl"
#endif
Name: "es"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "fr"; MessagesFile: "compiler:Languages\French.isl"
Name: "de"; MessagesFile: "compiler:Languages\German.isl"
Name: "it"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "ru"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "pt"; MessagesFile: "compiler:Languages\Portuguese.isl"
#if FileExists(AddBackslash(CompilerPath) + "Languages\Arabic.isl")
Name: "ar"; MessagesFile: "compiler:Languages\Arabic.isl"
#elif FileExists(AddBackslash(CompilerPath) + "Languages\Unofficial\Arabic.isl")
Name: "ar"; MessagesFile: "compiler:Languages\Unofficial\Arabic.isl"
#endif

[Tasks]
Name: "autostart"; Description: "Start at Windows sign-in"
Name: "startnow"; Description: "Start the agent now"

[Files]
Source: "{#BuildDir}\release\*"; DestDir: "{tmp}\release"; Flags: deleteafterinstall
Source: "..\..\agent\LICENSE"; DestDir: "{app}"; Flags: ignoreversion; AfterInstall: InstallAgent

[Icons]
Name: "{group}\Agent status"; Filename: "{app}\skynet-agent.exe"; Parameters: "launch status"; WorkingDir: "{app}"
Name: "{group}\Pause"; Filename: "{app}\skynet-agent.exe"; Parameters: "launch pause"; WorkingDir: "{app}"
Name: "{group}\Resume"; Filename: "{app}\skynet-agent.exe"; Parameters: "launch resume"; WorkingDir: "{app}"
Name: "{group}\Stop"; Filename: "{app}\skynet-agent.exe"; Parameters: "launch stop"; WorkingDir: "{app}"
Name: "{group}\Agent folder"; Filename: "{app}"
Name: "{group}\Uninstall"; Filename: "{uninstallexe}"

[UninstallDelete]
Type: filesandordirs; Name: "{app}\python"
Type: filesandordirs; Name: "{app}\versions"
Type: files; Name: "{app}\launcher.py"
Type: files; Name: "{app}\skynet-agent.cmd"
Type: files; Name: "{app}\skynet-agent.exe"
Type: files; Name: "{app}\launch-trial.json"
Type: files; Name: "{app}\release-policy.json"; Check: PurgeData
Type: files; Name: "{app}\release-history.json"; Check: PurgeData
Type: files; Name: "{app}\current.json"
Type: files; Name: "{app}\bad_seqs.json"; Check: PurgeData
Type: files; Name: "{app}\max_seq.json"; Check: PurgeData
Type: files; Name: "{app}\agent.lock"
Type: files; Name: "{app}\stop"
Type: files; Name: "{app}\identity.key"; Check: PurgeData
Type: filesandordirs; Name: "{app}\outbox"; Check: PurgeData
Type: filesandordirs; Name: "{app}\net"; Check: PurgeData
Type: filesandordirs; Name: "{app}\sent"; Check: PurgeData
Type: filesandordirs; Name: "{app}\logs"; Check: PurgeData
Type: files; Name: "{app}\config.json"; Check: PurgeData
Type: files; Name: "{app}\state.json"; Check: PurgeData
Type: files; Name: "{app}\task-list.json"; Check: PurgeData
Type: files; Name: "{app}\github-token"; Check: PurgeData
Type: dirifempty; Name: "{app}"

[Code]
var
  DeleteData: Boolean;
  UpdateGuard: TFileStream;

function AgentBusy: Boolean;
var
  Path: String;
  Stream: TFileStream;
begin
  Path := ExpandConstant('{app}\agent.lock');
  Result := FileExists(Path);
  if Result then
    try
      Stream := TFileStream.Create(Path, fmOpenRead or fmShareExclusive);
      Stream.Free;
      Result := False;
    except
      Result := True;
    end;
end;

function StopAgent: Boolean;
var
  I: Integer;
begin
  Result := not AgentBusy;
  if Result then exit;
  if not SaveStringToFile(ExpandConstant('{app}\stop'), 'stop' + #13#10, False) then exit;
  for I := 1 to 120 do begin
    Sleep(500);
    Result := not AgentBusy;
    if Result then exit;
  end;
end;

function PrepareToInstall(var NeedsRestart: Boolean): String;
begin
  Result := '';
  if not StopAgent then
    Result := 'The agent is still working. Wait for it to stop and retry.';
end;

procedure InstallAgent;
var
  Code: Integer;
  Args: String;
begin
  Args := ExpandConstant('install-bundle "{tmp}\release" "{app}"');
  if FileExists(ExpandConstant('{app}\python\python.exe')) then
    Args := Args + ExpandConstant(' "{app}\python\python.exe"');
  if not Exec(ExpandConstant('{tmp}\release\skynet-agent.exe'), Args, ExpandConstant('{app}'),
              SW_HIDE, ewWaitUntilTerminated, Code) or (Code <> 0) then
    RaiseException(Format('Signed installation failed (%d).', [Code]));
  if WizardIsTaskSelected('autostart') then
    if not Exec(ExpandConstant('{app}\skynet-agent.exe'), 'launch autostart enable', ExpandConstant('{app}'),
                SW_HIDE, ewWaitUntilTerminated, Code) or (Code <> 0) then
      RaiseException('Could not enable autostart.');
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  Code: Integer;
begin
  if (CurStep = ssPostInstall) and WizardIsTaskSelected('startnow') then
    if not Exec(ExpandConstant('{app}\skynet-agent.exe'), 'launch run',
                ExpandConstant('{app}'), SW_HIDE, ewNoWait, Code) then
      RaiseException(Format('Could not start the agent (%d).', [Code]));
end;

function PurgeData: Boolean;
begin
  Result := DeleteData;
end;

function InitializeUninstall: Boolean;
var
  Form: TSetupForm;
  Choice: TNewCheckBox;
  OK, Cancel: TNewButton;
begin
  Result := True;
  if not UninstallSilent then begin
    Form := CreateCustomForm(ScaleX(420), ScaleY(95), False, False);
    try
      Form.Caption := 'Uninstall SkyNet Agent';
      Choice := TNewCheckBox.Create(Form);
      Choice.Parent := Form;
      Choice.SetBounds(ScaleX(12), ScaleY(12), ScaleX(395), ScaleY(30));
      Choice.Caption := 'Delete the device key and saved data, including unsent results';
      Choice.Checked := False;
      OK := TNewButton.Create(Form);
      OK.Parent := Form;
      OK.SetBounds(ScaleX(235), ScaleY(56), ScaleX(78), ScaleY(25));
      OK.Caption := 'Continue';
      OK.ModalResult := mrOk;
      OK.Default := True;
      Cancel := TNewButton.Create(Form);
      Cancel.Parent := Form;
      Cancel.SetBounds(ScaleX(325), ScaleY(56), ScaleX(78), ScaleY(25));
      Cancel.Caption := 'Cancel';
      Cancel.ModalResult := mrCancel;
      Cancel.Cancel := True;
      Result := Form.ShowModal = mrOk;
      DeleteData := Result and Choice.Checked;
    finally
      Form.Free;
    end;
  end;
end;

procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
var
  RunKey: String;
begin
  RunKey := 'Software\Microsoft\Windows\CurrentVersion\Run';
  if CurUninstallStep = usUninstall then begin
    if not StopAgent then RaiseException('The agent is still working. Retry after it stops.');
    if FileExists(ExpandConstant('{app}\update.lock')) then
      UpdateGuard := TFileStream.Create(ExpandConstant('{app}\update.lock'), fmOpenReadWrite or fmShareExclusive);
    if RegValueExists(HKCU, RunKey, 'SkyNetAgent') and
       not RegDeleteValue(HKCU, RunKey, 'SkyNetAgent') then
      RaiseException('Could not disable autostart.');
  end else if CurUninstallStep = usPostUninstall then
    UpdateGuard.Free;
end;
