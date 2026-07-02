# Blender Tutorial - Creating a Rocket Launch Simulation

Source: https://www.youtube.com/watch?v=xjzhd62ZAKg
Caption track: English auto-generated
Duration: 22:30

[00:00] foreign [Music] and welcome to another blender made easy tutorial today we're going to be creating a rocket launch simulation to do this we're going to be using two different simulations one of them is for the smoke that shoots outwards and the

[00:29] other is for the actual rocket Trail and having two different simulations gives us much more control and allows us to tweak them individually so with that said let's go ahead and get started by deleting the default Cube and

[00:41] then of course we need to add in a rocket model now you can go ahead and create one of your own or you can use the one that I'm going to be using the link is in the description once you have it downloaded go over to file append and

[00:52] then navigate to where that blend file is mine is right here go underneath the source open up this blend file and go over to the object and select the bezier curve object and then append that in we can see it's way off in the distance so

[01:05] let's bring it back by hitting alt G or option G if you are on a Mac and then also it's rotated just so lightly so let's fix that by just rotating it just like that so it's going straight up now then of course I'm going to press Ctrl a

[01:18] and apply the scale and rotation just in case another thing I want to change is the look because currently it's using a pink material for the viewport so I'm going to come over here to the material tab select the main SMR and then scroll

[01:32] down to the viewport display and I'm just going to set it to White just so it's less just attracting and from there we can create the simulation now from here we need to animate the rocket moving upwards so I'm going to go into front view hit I and

[01:47] add in a location keyframe I'm also going to move this keyframe to let's go with frame 40. so it's going to start moving at frame 40. we're going to jump all the way over to frame 200 and then move this up let's move it up about

[02:01] 90 so press g z and type 90 and enter and that is pretty good then we'll hit I and add in another location keyframe so right now if we restart our simulation and play it you can see it starts to move up and then right about

[02:17] here you can see it slows down which is not very realistic so let's open up the graph editor and fix that I'm going to split this View and I did that by coming over to the top right corner clicking and dragging to split the window let's

[02:31] open up the graph editor and then to zoom this whole thing out you can press the home key on your keyboard and that'll Center everything up here we can see our animation data and you can see the curve when it slows down what we need to do is select the Z

[02:45] right here this is Z1 we're going to rotate this so that it's pointing downwards right about there then what you can also do is Select this bottom handle and position this how you want so probably something like this is pretty

[03:00] good so now let's restart this and take a look at it you can see it starts out slow starts to speed up and then right here it starts to go a lot faster which is pretty nice you can play around with this however you want if you want to be

[03:14] slower at the start just play around with it until you are happy with the results once you are ready you can go ahead and close this off and now let's create the actual smoke simulation we'll restart this and press shift a and we'll add an

[03:28] AQ this is going to be our domain object and the size of this I'm going to press n and underneath the dimensions let's set this up to 130 for both the X and the Y and for the Z we'll just drive this up so it's a bit taller and position it

[03:43] upwards now we need some flow objects so I'm going to press shift a and add in a circle go into edit mode and then press F to fill in that face so what we're going to be doing is having circles that surround this rocket and then shoot smoke

[03:57] outwards now there is a way to have the smoke directly from the exhaust of the engine shoot outwards but it doesn't go that far if we were to add that smoke right here it would probably end up like somewhere around here but I want the

[04:12] smoke to end up like way over here so the only way to really do that is to add in a flow object that's directly pointing to the right so that is why we're going to be adding in a circle so with this circle selected we'll go into front view go into edit

[04:27] mode and then we're just going to rotate it and place it right here or so go into top view something like that should be perfectly fine now another important thing is we need to make sure the normal of this circle is pointing in

[04:40] this direction we can check this by opening up this menu turning on the normal and dragging upwards and you can see that light blue line is pointing in that direction and that's what we want so next up let's just shift e this and

[04:53] place this all around I'm going to Shifty it rotate it this way kind of like at this angle maybe scale it double tap r to rotate it upwards a little bit let's go over to the physics panel and add in a fluid set the type over to flow

[05:13] and then for the flow Behavior we're going to select inflow what I want is right when the rocket starts to move up at frame 40. I want these flow objects to turn on so at frame 40 we're going to turn off the use flow and then add in a

[05:25] keyframe go over to the next frame frame 141 turn it on and then add in another keyframe then I want them to stop at a certain point so we're going to jump all the way over to frame 120 and that's when the rocket is right about that height we're

[05:43] going to add in another keyframe go over to the next frame and then turn it off so disable the use flow and then add in one last keyframe next up over in the velocity tab we're going to turn that on and then for the normal amount we're

[05:56] going to go all the way up to 90. with a value of 90 that means the smoke is going to have a lot of velocity right when it exits out of this flow object and that is exactly what we want and another thing that I'm going to do

[06:09] actually is duplicate all these objects and then place them a little bit further out because again right now with this smoke simulation set to 90 for the normal the smoke is going to shoot out probably around here or so but I want it

[06:22] to go even further so what we'll do is we'll just press shift d on this object go into edit mode and then drag these a little bit further out and scale them down slightly so we'll drag this one out here we'll press L to select that next Circle drag

[06:38] it out this way scale it down a little bit double tap r to rotate it something like that we'll grab this one L to select it move it out this way and scale it down so now that we have circles that are spread out even further the smoke is

[06:57] going to shoot out a lot more but we do need to change the settings on these what I want is for the normal amount to be a little bit less than the ones inside because the velocity is not going to be as strong let's go down to 50. and

[07:11] then also we need to make sure that these keyframes are moved over a little bit so the smoke from the center has time to actually reach this spot so let's move it over to frame 50.

[07:22] actually I think these circles are a bit too small so I'm going to go into edit mode on everything select everything by hitting a switch over to individual Origins and then just scale everything up just so they are a little bit bigger

[07:35] and I think that is better with that done select your domain object select fluid and set the type over to domain we're going to leave it on gas for the resolution divisions we're going to go up to 196.

[07:49] check the Border collisions along the bottom so the smoke collides with the bottom of the domain we'll turn on adaptive domain for the density and the heat values here we're going to bring them down to 0.7 so the smoke does not

[08:02] rise as quickly as for the noise we're also going to enable that we're going to set the upres factor down to 1 so it's not as high res and then for the strength we'll go down to 0.6 we're going to switch the type over to modular and then check on is resumable

[08:20] so we can bake in both the data up here and then the noise later and another important thing is we need to open up this collections Tab and select a individual collection for the flow objects since we're going to be having

[08:33] multiple domains in this simulation we need to separate them so select both of the flow objects select the domain object press M and move them to their own collection we'll call this outward smoke with the domain selected

[08:46] underneath the flow we're going to select the outward smoke so this means only the flow objects in this collection will affect this domain another important step is this cache folder right here if we add in another domain

[08:59] it's going to share this cache folder and we need to make sure they're separate so they don't overwrite each other select that button on the side and navigate to a folder which I've created right here called caches I've added two

[09:11] folders one for the outward smoke and one for the rocket Trail I'm going to select the outwards and accept and then with that done we are ready to bake in our simulation so with that done make sure you save your project select

[09:24] your domain and then click on bake data while the simulation is baking I wanted to let you guys know that I actually wrote a book on blender simulations it covers every physics-based simulation that blender has to offer in depth and I

[09:39] give examples for almost every setting and value it was a very long process to create and it required so much testing and practice but I'm really happy with how it turned out in every section of the book there are step-by-step projects

[09:51] that we go through to help you understand how to use blenders simulations and physics properly for example the fifth chapter is all about creating explosions and by the end of it you'll have created this animation if this is something that interests you

[10:05] I'll put the link to the ebook and the physical copy in the description and if you want to watch the trailer that I made for this book you can click in the top right corner right now so with that out of the way let's jump

[10:16] back to the tutorial all right I've stopped the bake at around 114 and here is our results if you don't see the smoke that's because you need to uncheck the noise if I enable it you can see it disappears so uncheck noise to see what your

[10:31] simulation looks like and as you can see that is looking really cool one issue though that I have is that this smoke is kind of pointed upwards and that's because this circle right here is also pointed upwards so to fix that I'm just

[10:44] going to go into edit mode select that Circle and double tap r so it's facing downwards like that and I think that will look a bit better and then also what I might do is with these uh with the circles in the center selected I

[10:59] might select this circle right here and then rotate this one just a little bit so it's pointing more towards this direction and then also another thing I forgot to mention is the end frame down here we need to set that to 200 as well we'll

[11:14] set that in the timeline to 200 so it matches with that done we are ready to bake this in so go ahead and click on bake and once that's done come down here to the noise and bake this in as well now it's time to create the actual

[11:26] rocket Trail to do this we're first going to restart the animation and then add in a new collection with a new domain so come over here to the top right add in a new collection by right clicking and then we'll name this collection smoke Trail then of course we

[11:39] need another domain object so let's add in another Cube we'll place this in the center by hitting alt G and then scaling it up pretty big as for the height of this we want it to be pretty tall so press n to open up the properties panel

[11:53] and underneath the X and Y will go with 50 and then 90 for the Z then we'll drag it up so it's sitting right about there that looks pretty good we'll skip to the end of the animation and see where the height of the rocket is and you can see

[12:07] it's right there so let's scale it up just a little bit so it's right underneath where the engine is next up for the flow objects we need to First add in a circle so add in a circle we'll place it in the center by hitting alt g

[12:20] go into edit mode and then of course we need to fill in a face so press F to fill in that face as for the size of this we're going to scale it up a little bit and then scale it along the X so it's a little bit wider something like

[12:32] that and then place it right at the center of the rocket that is looking pretty good let's also drag it up so it's right underneath the exhaust right about there is good scale it up a little bit then we need to parent it to

[12:45] this rocket so with that object selected select the rocket press Ctrl or command p and then click on object so now as the rocket goes up the flow object will also go with it then with this object selected let's give it a fluid set the type over to

[13:01] flow and we're going to be having two different flow objects one is for the smoke and one is for the fire so we'll call this one fire then we'll go over here and set the type over to fire for the flow Behavior we're going to select inflow the initial

[13:16] velocity we're also going to enable and then for the Z direction we're going to go with a very high value of negative 200.

[13:24] so the fire is going to be shooting downwards very very quickly as for the other object we're going to press shift d on it we're going to scale it up just a little bit and then this object is going to be the smoke so we'll

[13:36] double tap here and call it smoke for the flow type change it over to smoke and then I do want it to be negative 200 for a little bit but then I want it to even out so what we're going to do is jump all the way to frame 70 right here set the

[13:52] initial velocity We'll add an a keyframe oh this is supposed to be on 70 not 90.

[13:57] so move it over to frame 70 then we're going to jump over to frame 80 set this to negative 10 and then add in another keyframe so over here right when it hits 80 it's going to just be negative 10 all the way through the entire animation and

[14:12] I found that looks a little bit better than having it at a negative 200 for the entire thing as for the domain settings let's go ahead and select it click on fluid and set the type over to domain also we need to make sure that these

[14:25] settings here that is planar is enabled since it's a flat object so open up the flow source is planar select the fire and turn on is planar jumping back over to the domain we're going to set the resolution again to 196.

[14:41] we're going to turn on the bottom and then turn on adaptive domain as for the buoyancy and heat values these are actually going to be negative values this will allow the smoke to actually sink down as the rocket is going up which gives it a cool look so

[14:58] let's set this to negative 0.5 we don't need any noise for this so go ahead and close that panel but we're also going to open up the fire panel and turn the vorticity of the Flames a bit lower this will give us less swirls in the fire and

[15:11] also a very important step is to select the flow collection so it doesn't take into account these flow objects here for the other domain so with the flow menu go ahead and click on smoke Trail so only the flow objects in the Smoke Trail

[15:24] will affect this domain we'll set the end frame to 200 then we also need to click on this button here to set a cache folder for all of the data I'm going to use my rocket folder that I created earlier then click accept we'll change the type over to modular so

[15:40] we can bake Everything at Once we'll click on is resumable and I think that is all we really need to do so with that done go ahead and save your project once again and then click on bake data once this is done we'll take a look at it and

[15:52] then we can create the material to see what our rocket Trail looks like let's jump to frame 140.

[15:59] and as you can see this is looking really cool if we jump even further to frame 180 we can see it even better and that is looking really nice as for the materials let's first create the one with the outward smoke so go ahead and

[16:12] select the domain we'll go into front view and actually let's set up the lighting so we can see the smoke a bit better for the lighting let's just add in a random HDR I'll put a link in the description of where you can get some

[16:23] really good high quality hdrs once you have downloaded one go ahead and select it and then open image let's set the strength of this to two and then also we're going to be rendering this in Cycles just because it looks a lot

[16:34] better in Cycles than in EV so jumping over to these Cycles Render engine I'm going to use my GPU then we'll press Z and go into rendered view looks like our rocket is missing some textures so an easy way to fix that is to go over to

[16:48] file down to external data and then find missing files navigate to where that rocket blend file is mine is right here go over to the textures and then find missing files I'm once you do that it should automatically import those back

[17:02] in and you should see it just like that select your domain and let's open up the Shader editor by again splitting this window and switching it over to the Shader editor let's give it a new material and then we don't need this principled

[17:15] Shader so go ahead and delete that and then add in a principled volume Shader we'll take the volume and plug it into the volume of the material output once we do this you should see some smoke appear in our scene there are a couple things that we need

[17:28] to do first off let's add in a volume info node we'll place that over here then we need a color ramp let's add in a color ramp and then finally we will add in a math node so go over to converter math node and we'll place that here

[17:42] we're going to take the density plug it into the color ramp the color into the value the Top Value and then the value is going to go into the density of the principled volume and then we also need to switch this over to multiply and now

[17:55] and now this value controls the density of the smoke let's go up to 25.

[18:01] another cool thing that we can do is with this color ramp if we drag this white value closer to the black value it'll clamp down on those transparent values in the smoke and make everything a bit more dense as you can see there

[18:14] that is looking really nice if you want the smoke to appear a bit more white we can come over here and set the color all the way up to White and then we can also set this value here to a little bit of a lower value let's go

[18:26] with negative 0.2 and once we do this this will allow more light to be absorbed into it which gives us a lighter color as you can see there if you go even further like 0.5 more light will appear but I think a value of about

[18:41] 0.3 or 0.2 works pretty well as for the rocket Trail domain we're going to basically do the exact same thing here so let's go ahead and name this material smoke then we will select our bigger domain here with this drop down menu

[18:55] select the material smoke we don't want to change anything for this material so go ahead and duplicate it by hitting that two button and then let's add in the fire by pressing shift a we'll go over to search and we'll type

[19:09] in black body we're going to take this color and plug it directly into the emission strength then we're going to take this multiply node Shifty it drop it down here we'll take the flame attribute from the volume inflow and plug it into the the

[19:24] top input then the value is going to go into the emission strength and once we do this you should see the fire appear in your scene to control this a bit more we can add in another color ramp so Shifty it place it right here and then

[19:37] what we can do is clamp down on some of those light values if we drag the black closer it'll get rid of some of that light value then if we drag the white closer it'll make them a bit brighter so let's go into front view to see exactly

[19:50] what that looks like as you can see that is looking pretty good so far I might drag it a little bit more and also the density of our smoke here is a bit too much so let's bring this down to 10.

[20:04] just so the fire appears a bit brighter in our scene and if you want to see exactly what the fire looks like set this density to zero and you can see the Flames I think the trail is a bit too long so I'm going to drag this down even

[20:17] further something like that is going to look pretty good then we can set this back up to 10.

[20:25] if you want it to be brighter you can set this value here let's go with a value of 50 to see what that looks like and then finally one last thing if we jump over to the render settings panel underneath the color management we can

[20:37] set the look of this to high contrast to make the colors just pop a bit more and there we go that looks really nice again if you want to clamp down on the smoke here you can drag this this way drag this this way and you can clamp

[20:52] down on the amount of smoke for the rocket Trail so if you want more fire to appear you can play around with this color ramp but I think that is looking really nice another way to play around with the color of the fire is with this

[21:05] temperature value if you go up to let's say like 2000 or so it's going to be more of a yellowish color if you go lower like 1000 it's going to be more of a reddish color and then in between is like an orange color I found that a

[21:18] value of about 1500 or let's say 1700 I think that's actually what I did for my scene looks pretty good in this case I think 1500 looks a little bit better so we have more of that orangish color so we're going to leave it right there but

[21:31] you can play around with it if you want you can also just go ahead and disillocate this as well and change the emission color if you want a blue rocket Trill a green one you can do that here with this emission color I like this look so I'm going to plug

[21:44] that back into the emission for rendering this animation I found that you don't really need too many samples you can actually go with a very low sample count for my scene I think I went with a value of about 50 or so but you

[21:57] can get away with 25 and it will still look good with the denoise enabled so for this scene I'm going to go with 50 but there we go guys that is the end of this tutorial from here you can set an output folder render it into an

[22:08] animation and if you created something I would love to see it so make sure to send to me on Instagram at blender made easy if you have other ideas for tutorials you would like to see in the future let me know in the comments down below but

[22:21] that's going to be it I will see you guys in the next one foreign