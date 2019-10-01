resource "digitalocean_droplet" "trd-docker-1" {
    image = "coreos-stable"
    name = "trd-docker-1"
    region = "nyc3"
    size = "c-4"
    private_networking = true
    ssh_keys = [
        "${var.ssh_fingerprint}"
    ]

    connection {
        user = "core"
        type = "ssh"
        private_key = "${file(var.pvt_key)}"
        timeout = "10m"
    }
    
    provisioner "file" {
        source = "${var.pvt_key}"
        destination = "~/.ssh/id_rsa"
    }

    provisioner "remote-exec" {
        inline = [
            "cd",
            "chmod 600 ~/.ssh/id_rsa",
            "ssh-keyscan -H github.com >> ~/.ssh/known_hosts",
            "git config --global user.email \"${var.user_email}\"",
            "git config --global user.name \"${var.user_name}\"",
            "git clone ssh://git@github.com/ReformedDevs/challenge-2019-10",
            "cd challenge-2019-10",
            "git checkout -b update-leaderboard",
            "./build_docker.sh",
            "./run_docker.sh",
            "git commit -am \"Updated leaderboard and results json.\"",
            "git push --set-upstream origin update-leaderboard"
        ]
    }
}