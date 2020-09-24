![](https://files.peakd.com/file/peakd-hive/engrave/IHxPwBD1-hiveprojects_update.png)

# What is Hive Projects?

Hive Projects is the biggest directory of apps, sites, tools, and scripts created for the Hive ecosystem. This website is an entirely volunteer-driven effort. That includes coding time and hosting costs. If you wish to help or show your gratitude, there are plenty of ways in which you can do that:
 * upvote this post
 * reblog or cross-post it into your favorite community
 * contribute to HiveProjects, by adding a new project - everyone can do it!
 * let us know about new project, by posting about it in [Hive Projects Community](https://peakd.com/c/hive-192847) or by cross-posting to it or simply paste us a link at [Engrave Discord server](https://discord.gg/8NktdFh)
 * vote for our @engrave witness
 * write a comment :)

***

{% if last_post %}
Previous post: [{{ last_post.title }}]({{ last_post.link }})

***
{% endif %}


# Newly added projects 

{% for item in items %}

## {{ item.project.name }}
**Team:** {{ item.hive_team_members }}

![]({{ item.project_image_url }})

**Category:** [{{item.category_name}}]({{item.category_url}})

**Description:** *{{ item.project.description }}*

[{{item.project.name}} on HiveProjects.io]({{item.project_url}})

{% endfor %}

***

<center>

**That would be all for today. Stay tuned for the next update and consider contributing to Hive Projects. It is a community-driven website.**

**Click on the image to vote for @engrave witness:**

[![banner_engrave 100.png](https://images.hive.blog/DQmUghvic5TCPPvVkB4iB7eXmgQ3RQ4L8jkVizvuCBW8RMT/banner_engrave%20100.png)](https://hivesigner.com/sign/account-witness-vote?witness=engrave&approve=1)

**Dont forget to follow @engrave account!**

</center>
