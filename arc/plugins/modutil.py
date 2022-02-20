# Arc is copyright 2009-2011 the Arc team and other contributors.
# Arc is licensed under the BSD 2-Clause modified License.
# To view more details, please see the "LICENSING" file in the "docs" folder of the Arc Package.

import cPickle

from arc.includes.mcbans_api import McBans

from arc.constants import *
from arc.decorators import *
from arc.plugins import *

class ModUtilPlugin(ProtocolPlugin):
    commands = {
        "srb": "commandSRB",
        "srs": "commandSRS",
        "u": "commandUrgent",
        "urgent": "commandUrgent",

        "banish": "commandBanish",
        "worldkick": "commandBanish",
        "worldban": "commandWorldBan",
        "unworldban": "commandUnWorldban",
        "deworldban": "commandUnWorldban",
        "worldbanned": "commandWorldBanned",

        "ban": "commandBan",
        "banb": "commandBanBoth",
        "ipban": "commandIpban",
        "ipreason": "commandIpreason",
        "kick": "commandKick",
        "banreason": "commandReason",
        "unban": "commandUnban",
        "unipban": "commandUnipban",
        "banned": "commandBanned",
        "freeze": "commandFreeze",
        "stop": "commandFreeze",
        "unfreeze": "commandUnFreeze",
        "defreeze": "commandUnFreeze",
        "unstop": "commandUnFreeze",

        "hide": "commandHide",

        "overload": "commandOverload",
        "send": "commandSend",

        "spectate": "commandSpectate",
        "follow": "commandSpectate",
        "watch": "commandSpectate",

        "silence": "commandSilence",
        "desilence": "commandDesilence",
        "unsilence": "commandDesilence",
        "silenced": "commandSilenced",
        }

    hooks = {
        "playerpos": "playerMoved",
        "poschange": "posChanged",
        }

    def gotClient(self):
        self.hidden = False
        self.spectating = False

    def playerMoved(self, x, y, z, h, p):
        "Stops transmission of user positions if hide is on."
        if self.hidden:
            return False

    def posChanged(self, x, y, z, h, p):
        "Hook trigger for when the user moves"
        for uid in self.client.factory.clients:
            user = self.client.factory.clients[uid]
            try:
                if user.spectating == self.client.id:
                    if user.x != x and user.y != y and user.z != z:
                        user.teleportTo(x >> 5, y >> 5, z >> 5, h, p)
            except AttributeError:
                pass

    def loadRank(self):
        file = open('config/data/titles.dat', 'r')
        rank_dic = cPickle.load(file)
        file.close()
        return rank_dic

    def dumpRank(self, bank_dic):
        file = open('config/data/titles.dat', 'w')
        cPickle.dump(bank_dic, file)
        file.close()

    @config("rank", "director")
    def commandSRB(self, parts, fromloc, overriderank):
        "/srb [reason] - Director\nPrints out a reboot message."
        self.client.factory.sendMessageToAll(
            "%s[Server Reboot] %s" % (COLOUR_DARKRED, (" ".join(parts[1:]) if len(parts) > 1 else "Be back soon.")),
            "server", self.client)

    @config("rank", "director")
    def commandSRS(self, parts, fromloc, overriderank):
        "/srs [reason] - Director\nPrints out a shutdown message."
        self.client.factory.sendMessageToAll(
            "%s[Server Shutdown] %s" % (COLOUR_DARKRED, (" ".join(parts[1:]) if len(parts) > 1 else "See you later.")),
            "server", self.client)

    @config("rank", "admin")
    def commandUrgent(self, parts, fromloc, overriderank):
        "/u message - Admin\nAliases: urgent\nPrints out message in the server color."
        if len(parts) == 1:
            self.client.sendServerMessage("Please type a message.")
        else:
            self.client.factory.sendMessageToAll("%s[URGENT] %s" % (COLOUR_DARKRED, " ".join(parts[1:])), "server",
                self.client)

    @config("category", "player")
    @config("rank", "op")
    def commandWorldBanned(self, user, fromloc, overriderank):
        "/worldbanned - Op\nShows who is WorldBanned."
        if len(self.client.world.worldbans.keys()):
            self.client.sendServerList(["WorldBanned:"] + self.client.world.worldbans.keys())
        else:
            self.client.sendServerList(["WorldBanned: No one."])

    @config("category", "player")
    @config("rank", "op")
    @username_command
    @config("disabled_cmdblocks", True)
    def commandBanish(self, user, fromloc, overriderank):
        "/worldkick username - Op\nAliases: banish\nBanishes the user to the default world."
        if user.isWorldOwner() and not self.client.isMod():
            if user.isMod():
                self.client.sendServerMessage("You can't WorldKick a staff!")
            else:
                self.client.sendServerMessage("You can't WorldKick the world owner!")
            return
        else:
            if user.world == self.client.world:
                user.sendServerMessage("You were WorldKicked from '%s'." % self.client.world.id)
                user.changeToWorld("default")
                self.client.sendServerMessage("User %s got WorldKicked." % user.username)
            else:
                self.client.sendServerMessage("Your user is in another world!")

    @config("category", "player")
    @config("rank", "op")
    @only_username_command
    @config("disabled_cmdblocks", True)
    def commandWorldBan(self, username, fromloc, overriderank):
        "/worldban username - Op\nWorldBan a user from this world."
        if self.client.world.isWorldBanned(username):
            self.client.sendServerMessage("%s is already WorldBanned." % username)
            return
        elif username == self.client.world.status["owner"].lower():
            self.client.sendServerMessage("You can't WorldBan the world owner!")
            return
        else:
            self.client.world.add_worldban(username)
            if username in self.client.factory.usernames:
                if self.client.factory.usernames[username].world == self.client.world:
                    self.client.factory.usernames[username].changeToWorld("default")
                    self.client.factory.usernames[username].sendServerMessage("You got WorldBanned!")
            self.client.sendServerMessage("%s has been WorldBanned." % username)

    @config("category", "player")
    @config("rank", "op")
    @only_username_command
    def commandUnWorldban(self, username, fromloc, overriderank):
        "/unworldban username - Op\nAliases: deworldban\nRemoves the WorldBan on the user."
        if not self.client.world.isWorldBanned(username):
            self.client.sendServerMessage("%s is not WorldBanned." % username)
        else:
            self.client.world.delete_worldban(username)
            self.client.sendServerMessage("%s was UnWorldBanned." % username)

    @config("category", "player")
    @config("rank", "op")
    def commandHide(self, params, fromloc, overriderank):
        "/hide - Op\nAliases: cloak\nHides you so no other users can see you. Toggle."
        if not self.hidden:
            self.client.sendServerMessage("You have vanished.")
            self.hidden = True
            # Send the "user has disconnected" command to people
            self.client.queueTask(TASK_PLAYERLEAVE, [self.client.id]) # Skipmsg = true
        else:
            self.client.sendServerMessage("That was Magic!")
            self.hidden = False
            # Imagine that! They've mysteriously appeared.
            self.client.queueTask(TASK_NEWPLAYER,
                [self.client.id, self.client.username, self.client.x, self.client.y, self.client.z, self.client.h,
                 self.client.p])

    @config("category", "player")
    @config("rank", "mod")
    def commandBanned(self, user, fromloc, overriderank):
        "/banned - Mod\nShows who is Banned."
        done = ""
        for element in self.client.factory.banned.keys():
            done = done + " " + element
        if len(done):
            self.client.sendServerList(["Banned:"] + done.split(' '))
        else:
            self.client.sendServerList(["Banned: No one."])

    @config("category", "player")
    @config("rank", "helper")
    def commandSilenced(self, parts, fromloc, overriderank):
        "/silenced - Helper\nLists all Silenced players."
        if len(self.client.factory.silenced):
            self.client.sendServerList(["Silenced:"] + list(self.client.factory.silenced))
        else:
            self.client.sendServerList(["Silenced:"] + list("N/A"))

    @config("category", "player")
    @config("rank", "helper")
    @username_command
    @config("disabled_cmdblocks", True)
    def commandKick(self, user, fromloc, overriderank, params=[]):
        "/kick username [reason] - Helper\nKicks the user off the server."
        username = user.username
        if params:
            user.sendError("Kicked by %s: %s" % (self.client.username, " ".join(params)))
        else:
            user.sendError("You got kicked by %s." % self.client.username)
        self.client.sendServerMessage("User %s kicked." % username)

    @config("category", "player")
    @config("rank", "mod")
    @config("disabled_cmdblocks", True)
    def commandBanBoth(self, parts, fromloc, overriderank):
        "/banb username reason - Mod\nName and IP ban a user from this server, and on MCBans."
        if len(parts) <= 2:
            self.client.sendServerMessage("Please specify a username and a reason.")
            return
            # Grab statistics
        username = parts[1].lower()
        if username not in self.client.factory.usernames:
            noIP = True
        else:
            noIP = False
            ip = self.client.factory.usernames[username].transport.getPeer().host
            # Region MCBans
        if self.client.factory.serverPluginExists("McBansServerPlugin"):
            if not noIP:
                try:
                    value = self.client.factory.serverPlugins["McBansServerPlugin"].handler.globalBan(username, ip,
                        " ".join(parts[2:]), self.client.username)
                except Exception as e:
                    self.client.sendServerMessage("Error when banning user globally on MCBans.")
                    self.client.sendServerMessage(str(e))
                else:
                    if value["result"] == u'y':
                        self.client.sendServerMessage("%s has been banned on MCBans." % username)
                    else:
                        self.client.sendServerMessage("MCBans was unable to process this request.")
                        self.client.sendServerMessage("Please check MCBans for more info.")
            else:
                self.client.sendServerMessage("User %s is not online, unable to submit to MCBans." % username)
        else:
            self.client.sendServerMessage("MCBans server plugin not loaded, skipping this part.")
            # Region ban
        if self.client.factory.isBanned(username):
            self.client.sendServerMessage("%s is already banned." % username)
        else:
            self.client.factory.addBan(username, " ".join(parts[2:]), self.client.username)
            self.client.sendServerMessage("Player %s banned. Continuing to IPBan..." % username)
            # Region IPBan
        if not noIP:
            if self.client.factory.isIpBanned(ip):
                self.client.sendServerMessage("%s is already IPBanned." % ip)
                return
            else:
                self.client.sendServerMessage("%s has been IPBanned." % ip)
                self.client.factory.addIpBan(ip, " ".join(parts[2:]))
        else:
            self.client.sendServerMessage("User %s is not online, unable to IPBan." % username)
            # Follow-up action
        if username in self.client.factory.usernames:
            self.client.factory.usernames[username].sendError(
                "You got IPbanned by %s: %s" % (self.client.username, " ".join(parts[2:])))

    @config("category", "player")
    @config("rank", "mod")
    @config("disabled_cmdblocks", True)
    def commandBan(self, parts, fromloc, overriderank):
        "/ban username reason - Mod\nBans the player from this server."
        if len(parts) <= 2:
            self.client.sendServerMessage("Please specify a username and a reason.")
            return
        username = parts[1]
        if self.client.factory.isBanned(username):
            self.client.sendServerMessage("%s is already banned." % username)
        else:
            self.client.factory.addBan(username, " ".join(parts[2:]), self.client.username)
            if username in self.client.factory.usernames:
                self.client.factory.usernames[username].sendError(
                    "You got banned by %s: %s" % (self.client.username, " ".join(parts[2:])))
            self.client.sendServerMessage("%s has been banned for %s." % (username, " ".join(parts[2:])))

    @config("category", "player")
    @config("rank", "mod")
    @config("disabled_cmdblocks", True)
    def commandIpban(self, parts, fromloc, overriderank):
        "/ipban username reason - Mod\nBan a user's IP from this server."
        if parts[1].lower() not in self.client.factory.usernames:
            self.client.sendServerMessage("Sorry, that user is not online.")
            return
        username = parts[1].lower()
        ip = self.client.factory.usernames[username].transport.getPeer().host
        if self.client.factory.isIpBanned(ip):
            self.client.sendServerMessage("%s is already IPBanned." % ip)
        else:
            if len(parts) <= 2:
                self.client.sendServerMessage("Please specify a username and a reason.")
                return
            else:
                self.client.sendServerMessage("%s has been IPBanned." % ip)
                self.client.factory.addIpBan(ip, " ".join(parts[2:]))
                if username in self.client.factory.usernames:
                    self.client.factory.usernames[username].sendError(
                        "You got IPbanned by %s: %s" % (self.client.username, " ".join(parts[2:])))

    @config("category", "player")
    @config("rank", "mod")
    @only_username_command
    def commandUnban(self, username, fromloc, overriderank):
        "/unban username - Mod\nRemoves the Ban on the user."
        if not self.client.factory.isBanned(username):
            self.client.sendServerMessage("%s is not banned." % username)
        else:
            self.client.factory.removeBan(username)
            self.client.sendServerMessage("%s has been unbanned." % username)

    @config("category", "player")
    @config("rank", "admin")
    @only_string_command("IP")
    def commandUnipban(self, ip, fromloc, overriderank):
        "/unipban ip - Admin\nRemoves the Ban on the IP."
        if not self.client.factory.isIpBanned(ip):
            self.client.sendServerMessage("%s is not Banned." % ip)
        else:
            self.client.factory.removeIpBan(ip)
            self.client.sendServerMessage("%s UnBanned." % ip)

    @config("category", "player")
    @config("rank", "mod")
    @only_username_command
    def commandReason(self, username, fromloc, overriderank):
        "/banreason username - Mod\nGives the reason a user was Banned."
        if not self.client.factory.isBanned(username):
            self.client.sendServerMessage("%s is not Banned." % username)
        else:
            self.client.sendServerMessage("Reason: %s" % self.client.factory.banReason(username))

    @config("category", "player")
    @config("rank", "admin")
    @only_string_command("IP")
    def commandIpreason(self, ip, fromloc, overriderank):
        "/ipreason username - Admin\nGives the reason an IP was Banned."
        if not self.client.factory.isIpBanned(ip):
            self.client.sendServerMessage("%s is not Banned." % ip)
        else:
            self.client.sendServerMessage("Reason: %s" % self.client.factory.ipBanReason(ip))

    @config("category", "player")
    @config("rank", "mod")
    def commandUnFreeze(self, parts, fromloc, overriderank):
        "/unfreeze username - Mod\nAliases: defreeze, unstop\nUnfreezes the user, allowing them to move again."
        try:
            username = parts[1]
        except:
            self.client.sendServerMessage("No username given.")
            return
        try:
            user = self.client.factory.usernames[username]
        except:
            self.client.sendServerMessage("User is not online.")
            return
        user.frozen = False
        user.sendNormalMessage("&4You have been unfrozen by %s!" % self.client.username)

    @config("category", "player")
    @config("rank", "mod")
    @config("disabled_cmdblocks", True)
    def commandFreeze(self, parts, fromloc, overriderank):
        "/freeze username - Mod\nAliases: stop\nFreezes the user, preventing them from moving."
        try:
            username = parts[1]
        except:
            self.client.sendServerMessage("No username given.")
            return
        try:
            user = self.client.factory.usernames[username]
        except:
            self.client.sendServerMessage("User is not online.")
            return
        user.frozen = True
        user.sendNormalMessage("&4You have been frozen by %s!" % self.client.username)

    @config("category", "player")
    @config("rank", "admin")
    @username_command
    @config("disabled_cmdblocks", True)
    def commandOverload(self, client, fromloc, overriderank):
        "/overload username - Admin\nSends the users client a massive fake world."
        client.sendOverload()
        self.client.sendServerMessage("Overload sent to %s." % client.username)

    @config("category", "player")
    @config("rank", "mod")
    @config("disabled_cmdblocks", True)
    def commandSend(self, parts, fromloc, overriderank):
        "/send username world - Mod\nSends the users client to another world."
        if len(parts) < 2:
            self.client.sendServerMessage("Pleasey specify the username and the world.")
            return
        username = parts[1]
        world_id = parts[2]
        if not self.client.factory.world_exists(world_id):
            self.client.sendServerMessage("That world does not exist.")
            return
        elif username not in self.client.factory.usernames:
            self.client.sendServerMessage("User %s is not online." % username)
            return
        elif self.client.factory.usernames[username].isMod() and not self.client.isMod():
            self.client.sendServerMessage("You cannot send staff!")
            return
        else:
            self.client.factory.usernames[username].changeToWorld(world_id)
            self.client.factory.usernames[username].sendServerMessage(
                "You were sent to %s by %s." % (world_id, self.client.username))
            self.client.sendServerMessage("User %s was sent to world %s." % (username, world_id))

    @config("category", "player")
    @config("rank", "mod")
    @only_username_command
    @config("disabled_cmdblocks", True)
    def commandSilence(self, username, byuser, overriderank):
        "/silence username - Mod\nDisallows the user to talk."
        if self.client.factory.isMod(username):
            self.client.sendServerMessage("You cannot silence staff!")
            return
        self.client.factory.silenced.add(username)
        self.client.sendServerMessage("%s is now Silenced." % username)

    @config("category", "player")
    @config("rank", "mod")
    @only_username_command
    def commandDesilence(self, username, byuser, overriderank):
        "/desilence username - Mod\nAliases: unsilence\nAllows the user to talk."
        if self.client.factory.isSilenced(username):
            self.client.factory.silenced.remove(username)
            self.client.sendServerMessage("%s is no longer Silenced." % username.lower())
        else:
            self.client.sendServerMessage("They aren't silenced.")

    @config("rank", "op")
    @config("category", "player")
    @username_command
    def commandSpectate(self, user, fromloc, overriderank):
        "/spectate username - Guest\nAliases: follow, watch\nFollows specified user around"
        nospec_check = True
        try:
            getattr(self.client, "spectating")
        except AttributeError:
            nospec_check = False
        if not nospec_check or self.client.spectating != user.id:
            self.client.sendServerMessage("You are now spectating %s" % user.username)
            self.client.spectating = user.id
        else:
            self.client.sendServerMessage("You are no longer spectating %s" % user.username)
            self.client.spectating = False