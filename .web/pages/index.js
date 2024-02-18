/** @jsxImportSource @emotion/react */


import { Fragment, useCallback, useContext, useRef } from "react"
import { EventLoopContext, StateContexts, UploadFilesContext } from "/utils/context"
import { Event, getBackendURL, getRefValue, getRefValues, isTrue, refs, set_val } from "/utils/state"
import { Button as RadixThemesButton, Dialog as RadixThemesDialog, Flex as RadixThemesFlex, Heading as RadixThemesHeading, ScrollArea as RadixThemesScrollArea, Text as RadixThemesText, Theme as RadixThemesTheme } from "@radix-ui/themes"
import env from "/env.json"
import { Avatar, Box, Breadcrumb, BreadcrumbItem, Button, Drawer, DrawerBody, DrawerContent, DrawerHeader, DrawerOverlay, Flex, FormControl, Heading, HStack, Image as ChakraImage, Input, Link, Menu, MenuButton, MenuDivider, MenuItem, MenuList, Modal, ModalBody, ModalContent, ModalFooter, ModalHeader, ModalOverlay, Text, VStack } from "@chakra-ui/react"
import Script from "next/script"
import { CloseIcon, DeleteIcon, HamburgerIcon } from "@chakra-ui/icons"
import NextLink from "next/link"
import ReactDropzone from "react-dropzone"
import "@radix-ui/themes/styles.css"
import theme from "/utils/theme.js"
import { SpinningCircles } from "react-loading-icons"
import NextHead from "next/head"



export function Closeicon_11ed883525187cdaad471aef955f22dd () {
  const [addEvents, connectError] = useContext(EventLoopContext);

  const on_click_2905983f8758758258aab6a80fcc9a4c = useCallback((_e) => addEvents([Event("state.state.toggle_drawer", {})], (_e), {}), [addEvents, Event])

  return (
    <CloseIcon onClick={on_click_2905983f8758758258aab6a80fcc9a4c} sx={{"fontSize": "md", "color": "#fff8", "_hover": {"color": "#fff"}, "cursor": "pointer", "w": "8"}}/>
  )
}

export function Flex_90098c846fefa7a78ae981fcb13da1e4 () {
  const [filesById, setFilesById] = useContext(UploadFilesContext);


  return (
    <RadixThemesFlex align={`start`} css={{"flexDirection": "row"}} gap={`2`}>
  {(filesById.default ? filesById.default.map((f) => (f.path || f.name)) : []).map((children, props) => (
  <RadixThemesText as={`p`} key={props}>
  {children}
</RadixThemesText>
))}
</RadixThemesFlex>
  )
}

export function Box_97d1f8abdc2c15e2135cd714633c9ae3 () {
  
    const handleSubmit_a6fb427b7adf0f7db4d9b28324ef7e6f = useCallback((ev) => {
        const $form = ev.target
        ev.preventDefault()
        const form_data = {...Object.fromEntries(new FormData($form).entries()), ...{"question": getRefValue(refs['ref_question'])}}

        addEvents([Event("state.state.process_question", {form_data:form_data})])

        if (true) {
            $form.reset()
        }
    })
    
  const [addEvents, connectError] = useContext(EventLoopContext);


  return (
    <Box as={`form`} onSubmit={handleSubmit_a6fb427b7adf0f7db4d9b28324ef7e6f} sx={{"width": "100%"}}>
  <Formcontrol_939eaeffc75d989a7e4dacd3ee8319c9/>
</Box>
  )
}

export function Formcontrol_939eaeffc75d989a7e4dacd3ee8319c9 () {
  const state__state = useContext(StateContexts.state__state)
  const ref_question = useRef(null); refs['ref_question'] = ref_question;


  return (
    <FormControl isDisabled={state__state.processing}>
  <HStack sx={{"alignItems": "center", "justifyContent": "space-between"}}>
  <Input id={`question`} placeholder={`Type something...`} ref={ref_question} sx={{"background": "#262730", "borderColor": "#fff3", "borderWidth": "1px", "p": "4", "_placeholder": {"color": "#fffa"}, "_hover": {"borderColor": "#fffa"}}}/>
  <Button sx={{"background": "#ce4a4e", "borderColor": "#fff3", "borderWidth": "1px", "p": "4", "_hover": {"background": "#7f2225"}, "shadow": "rgba(95, 26, 55, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px, rgba(119, 104, 133, 0.35) 0px -2px 6px 0px inset;", "color": "#fff"}} type={`submit`}>
  <Fragment_182d151165b9fcd42b0e3549d1665960/>
</Button>
</HStack>
</FormControl>
  )
}

export function Button_38c35384972e8b7c4fe387f6d5088b12 () {
  const [addEvents, connectError] = useContext(EventLoopContext);

  const on_click_44ea287a5fe43aff33d47baeab2ad68c = useCallback((_e) => addEvents([Event("_call_script", {javascript_code:`refs['__clear_selected_files']('default')`})], (_e), {}), [addEvents, Event])

  return (
    <RadixThemesButton css={{"background": "#5ea09e"}} onClick={on_click_44ea287a5fe43aff33d47baeab2ad68c}>
  {`Clear`}
</RadixThemesButton>
  )
}

export function Button_8ae269be87b4d8ff7e1648aeec904542 () {
  const [addEvents, connectError] = useContext(EventLoopContext);
  const [filesById, setFilesById] = useContext(UploadFilesContext);

  const on_click_4e2d8f20ed65f854cae117923adec0c7 = useCallback((_e) => addEvents([Event("state.state.handle_upload", {files:filesById.default,upload_id:`default`}, "uploadFiles")], (_e), {}), [addEvents, Event, filesById, setFilesById])

  return (
    <RadixThemesButton css={{"background": "#5ea09e"}} onClick={on_click_4e2d8f20ed65f854cae117923adec0c7}>
  {`Upload`}
</RadixThemesButton>
  )
}

export function Box_ac1bd614b21a3bd657f85f0ce95694e7 () {
  const state__state = useContext(StateContexts.state__state)


  return (
    <Box>
  {state__state.chats[state__state.current_chat].map((qa, index_2f0915031b59136cfd0724124f2efcb1) => (
  <Box key={index_2f0915031b59136cfd0724124f2efcb1} sx={{"width": "100%"}}>
  <Box sx={{"textAlign": "right", "marginTop": "1em"}}>
  <Text sx={{"background": "#fff3", "shadow": "rgba(4, 3, 15, 0.15) 0px 48px 100px 0px;", "display": "inline-block", "p": "4", "borderRadius": "xl", "maxW": "30em"}}>
  {qa.question}
</Text>
</Box>
  <Box sx={{"textAlign": "left", "paddingTop": "1em"}}>
  <Text sx={{"background": "#5ea09e", "shadow": "rgba(4, 3, 15, 0.15) 0px 48px 100px 0px;", "display": "inline-block", "p": "4", "borderRadius": "xl", "maxW": "30em"}}>
  {qa.answer}
</Text>
</Box>
</Box>
))}
</Box>
  )
}

export function Button_3d311a7261a303c7b1a9953fd4706e2e () {
  const [addEvents, connectError] = useContext(EventLoopContext);

  const on_click_65775bd3c3ca6de4793090251b518aa6 = useCallback((_e) => addEvents([Event("state.state.create_chat", {})], (_e), {}), [addEvents, Event])

  return (
    <Button onClick={on_click_65775bd3c3ca6de4793090251b518aa6} sx={{"background": "#ce4a4e", "boxShadow": "md", "px": "4", "py": "2", "h": "auto", "_hover": {"background": "#7f2225"}, "shadow": "rgba(95, 26, 55, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px, rgba(119, 104, 133, 0.35) 0px -2px 6px 0px inset;", "color": "#fff"}}>
  {`Create`}
</Button>
  )
}

export function Text_329229aa15fcc43d0078f987bf0257b6 () {
  const state__state = useContext(StateContexts.state__state)


  return (
    <Text sx={{"size": "sm", "fontWeight": "normal"}}>
  {state__state.current_chat}
</Text>
  )
}

export function Fragment_1762bb90abdb81b879b2a22edbbe01a1 () {
  const [addEvents, connectError] = useContext(EventLoopContext);


  return (
    <Fragment>
  {isTrue(connectError !== null) ? (
  <Fragment>
  <RadixThemesDialog.Root open={connectError !== null}>
  <RadixThemesDialog.Content>
  <RadixThemesDialog.Title>
  {`Connection Error`}
</RadixThemesDialog.Title>
  <RadixThemesText as={`p`}>
  {`Cannot connect to server: `}
  {(connectError !== null) ? connectError.message : ''}
  {`. Check if server is reachable at `}
  {getBackendURL(env.EVENT).href}
</RadixThemesText>
</RadixThemesDialog.Content>
</RadixThemesDialog.Root>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  )
}

export function Input_a48e785f51ec00f1e9dc83de524369a7 () {
  const [addEvents, connectError] = useContext(EventLoopContext);

  const on_blur_655009403944aacdde6d38e4aa5f79da = useCallback((_e0) => addEvents([Event("state.state.set_new_chat_name", {value:_e0.target.value})], (_e0), {}), [addEvents, Event])

  return (
    <Input onBlur={on_blur_655009403944aacdde6d38e4aa5f79da} placeholder={`Type something...`} sx={{"background": "#262730", "borderColor": "#5F1A37", "_placeholder": {"color": "#776885"}}}/>
  )
}

export function Vstack_78bd184c4a6b3853917239c98b25dfe7 () {
  const state__state = useContext(StateContexts.state__state)
  const [addEvents, connectError] = useContext(EventLoopContext);


  return (
    <VStack alignItems={`stretch`} sx={{"alignItems": "stretch", "justifyContent": "space-between"}}>
  {state__state.chat_titles.map((chat, index_6799debebecd523c689edc1283428522) => (
  <HStack key={index_6799debebecd523c689edc1283428522} sx={{"color": "#fff", "cursor": "pointer"}}>
  <Box onClick={(_e) => addEvents([Event("state.state.set_chat", {chat_name:chat})], (_e), {})} sx={{"border": "double 1px transparent;", "borderRadius": "10px;", "backgroundImage": "linear-gradient(#04030F, #04030F), radial-gradient(circle at top left, #5ea09e,#ce4a4e);", "backgroundOrigin": "border-box;", "backgroundClip": "padding-box, border-box;", "p": "2", "_hover": {"backgroundImage": "linear-gradient(#04030F, #04030F), radial-gradient(circle at top left, #5ea09e,#5ea09e);"}, "color": "#fff8", "flex": "1"}}>
  {chat}
</Box>
  <Box sx={{"border": "double 1px transparent;", "borderRadius": "10px;", "backgroundImage": "linear-gradient(#04030F, #04030F), radial-gradient(circle at top left, #5ea09e,#ce4a4e);", "backgroundOrigin": "border-box;", "backgroundClip": "padding-box, border-box;", "p": "2", "_hover": {"backgroundImage": "linear-gradient(#04030F, #04030F), radial-gradient(circle at top left, #5ea09e,#5ea09e);"}}}>
  <DeleteIcon onClick={(_e) => addEvents([Event("state.state.delete_chat", {})], (_e), {})} sx={{"fontSize": "md", "color": "#fff8", "_hover": {"color": "#fff"}, "cursor": "pointer", "w": "8"}}/>
</Box>
</HStack>
))}
</VStack>
  )
}

export function Button_111ed3f8f32ad9df8152aad6fcb034cb () {
  const [addEvents, connectError] = useContext(EventLoopContext);

  const on_click_e9416bfe015c0fd3bcfc5ccef2e35037 = useCallback((_e) => addEvents([Event("state.state.toggle_modal", {})], (_e), {}), [addEvents, Event])

  return (
    <Button onClick={on_click_e9416bfe015c0fd3bcfc5ccef2e35037} sx={{"background": "#ce4a4e", "px": "4", "py": "2", "h": "auto", "shadow": "rgba(95, 26, 55, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px, rgba(119, 104, 133, 0.35) 0px -2px 6px 0px inset;", "color": "#fff", "_hover": {"background": "#ce4a4e"}}}>
  {`+ New Edit`}
</Button>
  )
}

export function Div_1abbeb603e7f6d61d699851b821583c9 () {
  const state__state__video_display_state = useContext(StateContexts.state__state__video_display_state)


  return (
    <div dangerouslySetInnerHTML={{"__html": state__state__video_display_state.dynamic_section}}/>
  )
}

export function Fragment_182d151165b9fcd42b0e3549d1665960 () {
  const state__state = useContext(StateContexts.state__state)


  return (
    <Fragment>
  {isTrue(state__state.processing) ? (
  <Fragment>
  <SpinningCircles height={`1em`}/>
</Fragment>
) : (
  <Fragment>
  <Text>
  {`Process`}
</Text>
</Fragment>
)}
</Fragment>
  )
}

export function Modal_93a91cd6ed9c6014ff375368e44387e0 () {
  const state__state = useContext(StateContexts.state__state)


  return (
    <Modal isOpen={state__state.modal_open}>
  <ModalOverlay>
  <ModalContent sx={{"background": "#1D1C27", "color": "#fff"}}>
  <ModalHeader>
  <HStack alignItems={`center`} justifyContent={`space-between`} sx={{"alignItems": "center", "justifyContent": "space-between"}}>
  <Text>
  {`Create new chat`}
</Text>
  <Closeicon_c90c6601ae2cde3940fecab2e59b2ad0/>
</HStack>
</ModalHeader>
  <ModalBody>
  <Input_a48e785f51ec00f1e9dc83de524369a7/>
</ModalBody>
  <ModalFooter>
  <Button_3d311a7261a303c7b1a9953fd4706e2e/>
</ModalFooter>
</ModalContent>
</ModalOverlay>
</Modal>
  )
}

export function Closeicon_c90c6601ae2cde3940fecab2e59b2ad0 () {
  const [addEvents, connectError] = useContext(EventLoopContext);

  const on_click_e9416bfe015c0fd3bcfc5ccef2e35037 = useCallback((_e) => addEvents([Event("state.state.toggle_modal", {})], (_e), {}), [addEvents, Event])

  return (
    <CloseIcon onClick={on_click_e9416bfe015c0fd3bcfc5ccef2e35037} sx={{"fontSize": "sm", "color": "#fff8", "_hover": {"color": "#fff"}, "cursor": "pointer"}}/>
  )
}

export function Hamburgericon_c98271a08d187d17b68bd3253ad088ed () {
  const [addEvents, connectError] = useContext(EventLoopContext);

  const on_click_2905983f8758758258aab6a80fcc9a4c = useCallback((_e) => addEvents([Event("state.state.toggle_drawer", {})], (_e), {}), [addEvents, Event])

  return (
    <HamburgerIcon onClick={on_click_2905983f8758758258aab6a80fcc9a4c} sx={{"mr": 4, "cursor": "pointer"}}/>
  )
}

export function Reactdropzone_aba04a9f504797db9188c90ac101ce9b () {
  const ref_default = useRef(null); refs['ref_default'] = ref_default;
  const [addEvents, connectError] = useContext(EventLoopContext);
  const [filesById, setFilesById] = useContext(UploadFilesContext);

  const on_drop_65dafcf47af23567d698a117f4553801 = useCallback(e => setFilesById(filesById => ({...filesById, default: e})), [addEvents, Event, filesById, setFilesById])

  return (
    <ReactDropzone id={`default`} multiple={true} onDrop={on_drop_65dafcf47af23567d698a117f4553801} ref={ref_default}>
  {({ getRootProps, getInputProps }) => (
    <Box sx={{"border": "1px dotted #5ea09e", "padding": "50px", "borderRadius": "lg"}} {...getRootProps()}>
    <Input type={`file`} {...getInputProps()}/>
    <VStack sx={{"alignItems": "stretch", "justifyContent": "space-between"}}>
    <RadixThemesButton css={{"background": "#ce4a4e", "borderColor": "#fff3", "borderWidth": "1px", "p": "4", "&:hover": {"background": "#7f2225"}}}>
    {`Select File`}
  </RadixThemesButton>
    <RadixThemesText as={`p`}>
    {`Drag and drop Stream here or Click to Select 📀`}
  </RadixThemesText>
  </VStack>
  </Box>
  )}
</ReactDropzone>
  )
}

export function Drawer_39c45250722aa9f02348e195ff653e70 () {
  const state__state = useContext(StateContexts.state__state)


  return (
    <Drawer isOpen={state__state.drawer_open} placement={`left`}>
  <DrawerOverlay>
  <DrawerContent sx={{"background": "#04030F", "color": "#fff", "opacity": "0.9"}}>
  <DrawerHeader>
  <HStack sx={{"alignItems": "center", "justifyContent": "space-between"}}>
  <Text>
  {`Chats`}
</Text>
  <Closeicon_11ed883525187cdaad471aef955f22dd/>
</HStack>
</DrawerHeader>
  <DrawerBody>
  <Vstack_78bd184c4a6b3853917239c98b25dfe7/>
</DrawerBody>
</DrawerContent>
</DrawerOverlay>
</Drawer>
  )
}

export default function Component() {

  return (
    <Fragment>
  <Fragment_1762bb90abdb81b879b2a22edbbe01a1/>
  <VStack alignItems={`stretch`} spacing={`0`} sx={{"background": "#04030F", "color": "#fff", "minH": "100vh", "alignItems": "stretch", "justifyContent": "space-between"}}>
  <Script src={`/custom_video_controls.js`} strategy={`afterInteractive`}/>
  <Box sx={{"backdropFilter": "auto", "backdropBlur": "lg", "p": "4", "position": "sticky", "top": "0", "zIndex": "100", "background": "rgba(255,255,255, 0.1)"}}>
  <HStack justify={`space-between`} sx={{"alignItems": "center", "justifyContent": "space-between"}}>
  <HStack sx={{"alignItems": "center", "justifyContent": "space-between"}}>
  <Hamburgericon_c98271a08d187d17b68bd3253ad088ed/>
  <Link as={NextLink} href={`/`}>
  <Box sx={{"p": "1", "borderRadius": "6", "background": "rgba(240, 240, 240, 0.2)", "mr": "2"}}>
  <ChakraImage src={`favicon.ico`} sx={{"width": 30, "height": "auto"}}/>
</Box>
</Link>
  <Breadcrumb>
  <BreadcrumbItem>
  <Heading size={`sm`}>
  {`Chopsticks`}
</Heading>
</BreadcrumbItem>
  <BreadcrumbItem>
  <Text_329229aa15fcc43d0078f987bf0257b6/>
</BreadcrumbItem>
</Breadcrumb>
</HStack>
  <HStack spacing={`8`} sx={{"alignItems": "center", "justifyContent": "space-between"}}>
  <Button_111ed3f8f32ad9df8152aad6fcb034cb/>
  <Menu sx={{"background": "#04030F", "border": "red"}}>
  <MenuButton>
  <Avatar name={`User`} size={`md`} sx={{"shadow": "rgba(95, 26, 55, 0.25) 0px 50px 100px -20px, rgba(0, 0, 0, 0.3) 0px 30px 60px -30px, rgba(119, 104, 133, 0.35) 0px -2px 6px 0px inset;", "color": "#fff", "background": "#5ea09e"}}/>
  <Box/>
</MenuButton>
  <MenuList sx={{"background": "#04030F", "border": "1.5px solid #ce4a4e"}}>
  <MenuItem sx={{"background": "#04030F", "color": "#fff"}}>
  {`Help`}
</MenuItem>
  <MenuDivider sx={{"border": "1px solid #ce4a4e"}}/>
  <MenuItem sx={{"background": "#04030F", "color": "#fff"}}>
  {`Settings`}
</MenuItem>
</MenuList>
</Menu>
</HStack>
</HStack>
</Box>
  <HStack spacing={`0`} sx={{"align": "stretch", "alignItems": "center", "justifyContent": "space-between"}}>
  <RadixThemesScrollArea css={{"height": "calc(100vh - 20vh)", "width": "80%", "borderRightWidth": "1px", "borderColor": "white"}} scrollbars={`vertical`} type={`always`}>
  <Flex direction={`column`} sx={{"spacing": "4"}}>
  <Box sx={{"flexGrow": "1", "paddingRight": "20px"}}>
  <HStack alignItems={`start`} justifyContent={`start`} spacing={`4`} sx={{"alignItems": "center", "justifyContent": "space-between"}}>
  <Box sx={{"width": "40%", "margin": "0px", "padding": "10px", "flexGrow": "1", "alignSelf": "start"}}>
  <VStack spacing={`4`} sx={{"alignItems": "stretch", "justifyContent": "space-between"}}>
  <Reactdropzone_aba04a9f504797db9188c90ac101ce9b/>
  <Flex_90098c846fefa7a78ae981fcb13da1e4/>
  <Button_8ae269be87b4d8ff7e1648aeec904542/>
  <Button_38c35384972e8b7c4fe387f6d5088b12/>
  <Heading size={`lg`} sx={{"paddingTop": "10", "paddingBottom": "2", "align": "center"}}>
  {`What is this?`}
</Heading>
  <Text sx={{"paddingTop": "5", "paddingBottom": "5", "align": "center"}}>
  {`
        Chopsticks is the premier AI-powered editing software that utilizes deep learning to improve efficiency, 
        enhance user experience, and (amazingly) _increase_ creator profits.
        `}
</Text>
  <ChakraImage align={`center`} src={`/arrow.png`} sx={{"paddingTop": "5", "paddingBottom": "5", "width": "100px"}}/>
</VStack>
</Box>
  <Box sx={{"width": "60%", "borderRadius": "lg", "padding": "10px", "flexGrow": "1", "textAlign": "center", "background": "rgba(255,255,255, 0.1)", "alignItems": "center"}}>
  <Div_1abbeb603e7f6d61d699851b821583c9/>
</Box>
</HStack>
</Box>
</Flex>
</RadixThemesScrollArea>
  <RadixThemesScrollArea css={{"height": "calc(100vh - 20vh)", "width": "20%"}} scrollbars={`vertical`} type={`always`}>
  <Flex direction={`column`} sx={{"spacing": "4"}}>
  <VStack sx={{"py": "8", "flex": "1", "width": "100%", "maxW": "3xl", "paddingInlineStart": "4", "paddingInlineEnd": "4", "alignSelf": "center", "overflow": "hidden", "paddingBottom": "5em", "alignItems": "stretch", "justifyContent": "space-between"}}>
  <RadixThemesHeading align={`center`} weight={`medium`}>
  {`LLM powered Editor`}
</RadixThemesHeading>
  <Box_ac1bd614b21a3bd657f85f0ce95694e7/>
</VStack>
</Flex>
</RadixThemesScrollArea>
</HStack>
  <Box sx={{"position": "sticky", "bottom": "0", "left": "0", "py": "4", "backdropFilter": "auto", "backdropBlur": "lg", "alignItems": "stretch", "width": "100%", "background": "rgba(255,255,255, 0.1)"}}>
  <VStack sx={{"width": "100%", "maxW": "3xl", "mx": "auto", "alignItems": "stretch", "justifyContent": "space-between"}}>
  <Box_97d1f8abdc2c15e2135cd714633c9ae3/>
</VStack>
</Box>
  <Drawer_39c45250722aa9f02348e195ff653e70/>
  <Modal_93a91cd6ed9c6014ff375368e44387e0/>
</VStack>
  <NextHead>
  <title>
  {`Chopsticks`}
</title>
  <meta content={`A Reflex app.`} name={`description`}/>
  <meta content={`favicon.ico`} property={`og:image`}/>
</NextHead>
</Fragment>
  )
}
