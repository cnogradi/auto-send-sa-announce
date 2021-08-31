pipeline {
  agent any
    triggers {   
        URLTrigger( 
            cronTabSpec: 'H/15 * * * *',
            entries: [
                URLTriggerEntry( 
                    url: 'https://www.sermonaudio.com/search.asp?SourceOnly=true&currSection=sermonssource&keyword=${churchKey}&mediatype=MP4',
                    checkLastModificationDate: true,
                    checkETag: true,
                    contentTypes: [
                        MD5Sum()
                    ]
                )

            ])
    }
  stages {
    stage('Check for new sermons and send announcements') {
      steps {
        configFileProvider([configFile(fileId:'1b80bdec-4bad-410a-bcea-91af8fda88b3', targetLocation: 'config.json')]) {
            sh '''python3 auto-send-sa-announce.py'''
        }
      }
    }
  }
}