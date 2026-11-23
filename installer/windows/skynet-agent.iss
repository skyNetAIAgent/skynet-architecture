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
ArchitecturesAllowed=x64os
ArchitecturesInstallIn64BitMode=x64os
OutputDir={#BuildDir}\dist
OutputBaseFilename=SkyNetAgentSetup-{#AgentVersion}
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
Source: "{#BuildDir}\python\*"; DestDir: "{app}\python"; Flags: recursesubdirs ignoreversion; Check: InstallRuntime
Source: "{#BuildDir}\release\*"; DestDir: "{tmp}\release"; Flags: recursesubdirs deleteafterinstall
Source: "..\..\agent\LICENSE"; DestDir: "{app}"
Source: "..\..\agent\install.py"; DestDir: "{tmp}"; Flags: deleteafterinstall; AfterInstall: InstallAgent

[Icons]
Name: "{group}\Agent status"; Filename: "{cmd}"; Parameters: "/D /V:OFF /C "".\skynet-agent.cmd status & pause"""; WorkingDir: "{app}"
Name: "{group}\Pause"; Filename: "{app}\python\pythonw.exe"; Parameters: "-I ""{app}\launcher.py"" pause"
Name: "{group}\Resume"; Filename: "{app}\python\pythonw.exe"; Parameters: "-I ""{app}\launcher.py"" resume"
Name: "{group}\Stop"; Filename: "{app}\python\pythonw.exe"; Parameters: "-I ""{app}\launcher.py"" stop"
Name: "{group}\Agent folder"; Filename: "{app}"
Name: "{group}\Uninstall"; Filename: "{uninstallexe}"

[UninstallDelete]
Type: filesandordirs; Name: "{app}\python"
Type: filesandordirs; Name: "{app}\versions"
Type: files; Name: "{app}\launcher.py"
Type: files; Name: "{app}\skynet-agent.cmd"
Type: files; Name: "{app}\current.json"
Type: files; Name: "{app}\bad_seqs.json"
Type: files; Name: "{app}\max_seq.json"
Type: files; Name: "{app}\update.lock"
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
  KeepRuntime, DeleteData: Boolean;

function InstallRuntime: Boolean;
begin
  Result := not KeepRuntime;
end;

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
var
  Installed, Bundled: Int64;
begin
  if not StopAgent then begin
    Result := 'The agent is still working. Wait for it to stop and retry.';
    exit;
  end;
  if GetPackedVersion(ExpandConstant('{app}\python\python.exe'), Installed) and
     StrToVersion('{#RuntimeFileVersion}', Bundled) then
    KeepRuntime := ComparePackedVersion(Installed, Bundled) > 0;
end;

procedure RunPython(const Args: String);
var
  Code: Integer;
begin
  if not Exec(ExpandConstant('{app}\python\python.exe'), Args,
              ExpandConstant('{app}'), SW_HIDE, ewWaitUntilTerminated, Code) or (Code <> 0) then
    RaiseException(Format('Python failed (%d). See the setup log.', [Code]));
end;

procedure InstallAgent;
var
  Launcher: String;
begin
  RunPython(ExpandConstant('-I "{tmp}\install.py" --from-dir "{tmp}\release" --keep-newer --home "{app}"'));
  Launcher := ExpandConstant('-I "{app}\launcher.py" ');
  if WizardIsTaskSelected('autostart') then RunPython(Launcher + 'autostart enable')
  else RunPython(Launcher + 'autostart disable');
end;

procedure CurStepChanged(CurStep: TSetupStep);
var
  Code: Integer;
begin
  if (CurStep = ssPostInstall) and WizardIsTaskSelected('startnow') then
    if not Exec(ExpandConstant('{app}\python\pythonw.exe'), ExpandConstant('-I "{app}\launcher.py" run'),
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
    if RegValueExists(HKCU, RunKey, 'SkyNetAgent') and
       not RegDeleteValue(HKCU, RunKey, 'SkyNetAgent') then
      RaiseException('Could not disable autostart.');
  end;
end;
