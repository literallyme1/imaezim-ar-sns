import cv2
import numpy as np
from .models import ObjectDesc
#겹치는 특징점 제거 & 5000개 이하로 특징점
def filter_matching_features_orb(all_features):
    filtered_features = np.empty((0, 32), dtype=np.uint8) #[] #desc만
    ratio = 0.75
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING)
    for i in range(len(all_features)):
        if i == 0:
            filtered_features = np.append(filtered_features, all_features[0], axis=0) #
        else:
            matches = matcher.knnMatch(all_features[i], filtered_features, k=2) #500개 #all_features[i] 먼저
            bad_desc_Idx = [] #지금까지 저장된 특징점과 다른 특징점의 Idx
            # matches 리스트의 각 요소에 대해 반복
            for first, second in matches:
                if first.distance > second.distance * ratio: #distance: 매칭된 특징점 사이의 거리
                    bad_desc_Idx.append(first.queryIdx) #queryIdx: 매칭을 수행하는 기준이 되는 이미지의 특징점 인덱스
                                                        #trainIdx: 매칭 과정에서 비교 대상이 되는 이미지(학습이미지)의 특징점 인덱스
            #5000개 이상이면 그만
            f_number = filtered_features.shape[0]
            if f_number + len(bad_desc_Idx) > 5000:
                max_num = 5000 - f_number
                for Idx in bad_desc_Idx[:min(len(bad_desc_Idx), max_num)]:
                    filtered_features = np.append(filtered_features, [all_features[i][Idx]], axis=0)  # 다른 특징점 저장
                return filtered_features
            else:
                for Idx in bad_desc_Idx:
                    filtered_features = np.append(filtered_features, [all_features[i][Idx]], axis=0)  # 다른 특징점 저장
    return filtered_features

#물건 조회
def findObj(target):
    obj_id = [] #저장된 물건 id
    most_similar_obj_num = -1  # 가장 비슷한 물체 번호
    most_similar_obj_num_decs = -1  # 가장 많은 특징점 수
    target_desc = target[0]
    print(target_desc)
    # 저장 완료된 물체에서만 검색
    for i, object in enumerate([obj for obj in ObjectDesc.objects.all() if obj.registration_completed == True]):
        print(i)
        desc_path = object.desc.path
        print(desc_path)
        obj_id.append(object.id)
        npy_desc = np.load(desc_path)
        print(npy_desc)

        goodMatch = goodMatch_orb(target_desc, npy_desc)
        if most_similar_obj_num_decs < goodMatch:
            most_similar_obj_num_decs = goodMatch
            most_similar_obj_num = i

    if most_similar_obj_num == -1:
        return -1
    result_obj_id = obj_id[most_similar_obj_num]
    return result_obj_id  #조회된 obj id

def goodMatch_orb(desc, desc2):
    # 첫번재 이웃의 거리가 두 번째 이웃 거리의 75% 이내인 것만 추출
    ratio = 0.75
    # BF-Hamming 생성
    matcher = cv2.BFMatcher(cv2.NORM_HAMMING) #NORM_L2 -> sift, surf에 적합     #cv.NORM_HAMMING -> ORB에 적합
    matches = matcher.knnMatch(desc, desc2, k=2)
    good_matches = [first for first, second in matches \
                    if first.distance < second.distance * ratio]
    return len(good_matches)