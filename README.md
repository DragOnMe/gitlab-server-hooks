Introduction
================

My Server-Side Hook scripts for GitLab Server


## 스크립트 구성

Customized Server-side Hook은 다음의 3가지 중 하나로 구현되며, Shell script, Python, Rails 등
linux prompt 에서 수행 가능한 Script 언어로 구현된다

* pre-receive: Git 서버가 클라이언트로부터 Push 요청을 받은 즉시 수행되며, 스크립트에서 non-zero 값을
  return 하면 Push 요청은 reject 된다. Push 요청에 대한 값은 스크립트 내에서 stdin 스트림 값을 읽어서
  사용 가능하다.
* update: pre-receive 와 유사하지만, pre-receive 는 한 번의 Push에 대해 단 한 번 수행되며, update는
  각각의 Branch 마다 triggering 되는 점이 다르다. 따라서 여러 Branch에 Push 를 수행하게 되면 특정한
  Branch 에 대해서만 reject 되게 처리되게 하고 싶을 떄 사용한다.
* post-receive: Push 에 대한 모든 처리가 완료된 직후에 수행된다. Push 데이터에 대해 stdin 을 참조해서
  사용하면 되며,  주로 사용자에게 메일 발송이나 CI 서버로의 triggering 또는 이슈 트래킹 시스템으로
  Ticket을 업데이트할 때 사용한다.


## 사용 또는 운영 방법

 * 현재 pre-receive 만 python으로 구현되어 있다. 추가 기능이 필요할 경우 그에 맞게 추가/수정 사용한다
 * pre-receive-commit-msg-check.py 파일 최종 버전을 /root/custom_hooks_src에 저장해 둔다(백업/확인용, option 사항)
 * pre-receive-commit-msg-check.py 파일 최종 버전을 /root/custom_hooks 에 pre-receive 라는 이름으로 저장하고
   chmod a+x pre-receive, chown git.git pre-receive 로 설정한다
 * copy_custom_hooks.sh 스크립트의 target_path_list 에 pre-receive Hook 을 적용할 repository 정보를 등록한다
 * copy_custom_hooks.sh 파일을 적당한 위치에 저장(/root/copy_custom_hooks.sh)해 두고 실행하면
   지정된 repository 의 해당 path 로 복사된다


## 현재 pre-receive의 Git 클라이언트에서 commit 제약 조건

 * Commit message에 issue-123 또는 issue#123 또는 issue-#123 또는 hotfix 또는 force 가 없으면
   Remote 에 Push 시에 오류 발생함(대소문자 구분 없음)
 * Commit message 수정 방법은 git 클라이언트에 따라 다르며, 별도 표시하지 않음


## 참고: copy_custom_hooks.sh 내용

    #!/bin/bash
    #
    # * Copies custom_hooks directory to target repo path
    # * $GITREPO path is defined in .bash_profile
    #
    # Caution: one item per one line for clarity
    declare -a target_path_list=(
     "Group-or-Account/project-name-1.git"
     "Group-or-Account/project-name-2.git"
     "Project-name/repository-name.git"
     ...
    )
    
    for path in "${target_path_list[@]}"; do
      echo "Copying to: $path"
      cp -arf /root/custom_hooks/ $GITREPO/"$path"/
    done

