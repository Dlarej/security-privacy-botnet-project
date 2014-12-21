
class EmailAnalysis():

    def __init__(self, filename):
        self.text = ''
        with open(filename, 'r') as emailfile:
            self.text = emailfile.read()
        
        self.text = self.text.replace('-', ' ').lower()
        
        self.count = self.analyze()


    def analyze(self):
        count = {}
        for word in self.text.split():
            if word in count:
                count[word] += 1
            else:
                count[word] = 1
        return count

    def count_phrase(self, phrase):
        count = 0
        for line in self.text:
            print line
            if phrase in line:
                count += 1
        return count

if __name__ ==  '__main__':
    filename = '/home/matt/Dropbox/School Work/2014 Fall/Security and Privacy/Takeout/Mail/attack_emails.mbox'
    filename = 'attack_emails.mbox'
    analysis = EmailAnalysis(filename)
    print str(analysis.count['freshman']) + ' freshmen\n'
    print str(analysis.count['sophomore']) + ' sophomores\n'
    print str(analysis.count['junior']) + ' juniors\n'
    print str(analysis.count['senior']) + ' seniors\n'
    print str(analysis.count['graduated']) + ' alumni\n'
