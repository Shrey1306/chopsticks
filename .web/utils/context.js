import { createContext, useContext, useMemo, useReducer, useState } from "react"
import { applyDelta, Event, hydrateClientStorage, useEventLoop, refs } from "/utils/state.js"

export const initialState = {"state": {"is_hydrated": false, "router": {"session": {"client_token": "", "client_ip": "", "session_id": ""}, "headers": {"host": "", "origin": "", "upgrade": "", "connection": "", "pragma": "", "cache_control": "", "user_agent": "", "sec_websocket_version": "", "sec_websocket_key": "", "sec_websocket_extensions": "", "accept_encoding": "", "accept_language": ""}, "page": {"host": "", "path": "", "raw_path": "", "full_path": "", "full_raw_path": "", "params": {}}}}, "state.state": {"api_type": "openai", "chat_titles": ["Edit 1"], "chats": {"Edit 1": [{"question": "Upload an Image and Type to Edit. 🔥", "answer": "Go on!"}]}, "current_chat": "Edit 1", "drawer_open": false, "markers": [{"start": 1127.62, "end": 1161.58}, {"start": 312.18, "end": 346.48}, {"start": 1151.24, "end": 1183.42}, {"start": 351.1, "end": 391.5}, {"start": 307.5, "end": 342.14}, {"start": 256.34, "end": 290.84}, {"start": 252.5, "end": 287.0}, {"start": 154.38, "end": 188.04}], "modal_open": false, "new_chat_name": "", "processing": false, "question": "", "video_segments": []}, "state.state.video_display_state": {"dynamic_section": "<p style='font-size: large; padding: 50px;`'>Upload a Stream to Start Editing! ⏩</p>"}}

export const ColorModeContext = createContext(null);
export const UploadFilesContext = createContext(null);
export const DispatchContext = createContext(null);
export const StateContexts = {
  state: createContext(null),
  state__state: createContext(null),
  state__state__video_display_state: createContext(null),
}
export const EventLoopContext = createContext(null);
export const clientStorage = {"cookies": {}, "local_storage": {}}

export const onLoadInternalEvent = () => [Event('state.on_load_internal')]

export const initialEvents = () => [
    Event('state.hydrate', hydrateClientStorage(clientStorage)),
    ...onLoadInternalEvent()
]

export const isDevMode = true

export function UploadFilesProvider({ children }) {
  const [filesById, setFilesById] = useState({})
  refs["__clear_selected_files"] = (id) => setFilesById(filesById => {
    const newFilesById = {...filesById}
    delete newFilesById[id]
    return newFilesById
  })
  return (
    <UploadFilesContext.Provider value={[filesById, setFilesById]}>
      {children}
    </UploadFilesContext.Provider>
  )
}

export function EventLoopProvider({ children }) {
  const dispatch = useContext(DispatchContext)
  const [addEvents, connectError] = useEventLoop(
    dispatch,
    initialEvents,
    clientStorage,
  )
  return (
    <EventLoopContext.Provider value={[addEvents, connectError]}>
      {children}
    </EventLoopContext.Provider>
  )
}

export function StateProvider({ children }) {
  const [state, dispatch_state] = useReducer(applyDelta, initialState["state"])
  const [state__state, dispatch_state__state] = useReducer(applyDelta, initialState["state.state"])
  const [state__state__video_display_state, dispatch_state__state__video_display_state] = useReducer(applyDelta, initialState["state.state.video_display_state"])
  const dispatchers = useMemo(() => {
    return {
      "state": dispatch_state,
      "state.state": dispatch_state__state,
      "state.state.video_display_state": dispatch_state__state__video_display_state,
    }
  }, [])

  return (
    <StateContexts.state.Provider value={ state }>
    <StateContexts.state__state.Provider value={ state__state }>
    <StateContexts.state__state__video_display_state.Provider value={ state__state__video_display_state }>
      <DispatchContext.Provider value={dispatchers}>
        {children}
      </DispatchContext.Provider>
    </StateContexts.state__state__video_display_state.Provider>
    </StateContexts.state__state.Provider>
    </StateContexts.state.Provider>
  )
}